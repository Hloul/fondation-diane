# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
import io
import re
import requests
import PyPDF2
import json
import mimetypes

from PIL import Image
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import Warning, UserError, AccessError
from werkzeug import urls
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import url_for

class Slide(models.Model):
    _inherit = 'slide.slide'
    _name = 'slide.slide'

    additional_type = fields.Selection(selection=[
        ('googledrivevideo', 'Google Drive video (put long id, example: 1oOIeTJwf4CWTRmcOONtTigfGDQpCMHPe)'),
        ('clapprvideo', 'External video (mp4, etc, livestream m3u8 and other supported formats)'),
        ('vimeovideo', 'Vimeo Video'),
        ('localvideo', 'Local Video (Ensure upload size limit in your server)'),
        ("zoom_meeting","Zoom Meeting")], string="Aditional type")
    zoom_meeting_ID = fields.Char(string="Meeting ID")
    zoom_meeting_name = fields.Char(string="Zoom Meeting Name", placeholder="Paste Here Zoom Meeting Name")
    video_data = fields.Binary(string="Upload video (mp4/webm/ogv)")
    is_localvideo = fields.Boolean(string="Local Video (Uploaded)", default=False)

    def _get_embed_code(self):
        base_url = request and request.httprequest.url_root or self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        for record in self:
            if record.datas and (not record.document_id or record.slide_type in ['document', 'presentation']):
                slide_url = base_url + url_for('/slides/embed/%s?page=1' % record.id)
                record.embed_code = '<iframe src="%s" class="o_wslides_iframe_viewer" allowFullScreen="true" height="%s" width="%s" frameborder="0"></iframe>' % (
                slide_url, 315, 420)
            elif record.slide_type == 'video' and record.document_id:
                if not record.mime_type:
                    if not record.additional_type:
                        # embed youtube video
                        query = urls.url_parse(record.url).query
                        query = query + '&theme=light' if query else 'theme=light'
                        record.embed_code = '<iframe src="//www.youtube-nocookie.com/embed/%s?%s" allowFullScreen="true" frameborder="0"></iframe>' % (
                        record.document_id, query)
                    else:
                        if record.additional_type == 'vimeovideo':
                            # embed vimeo video
                            content_url = 'https://player.vimeo.com/video/' + record.document_id
                            record.embed_code = '<iframe class="vimeoVideo" src="' + content_url + '" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'
                        if record.additional_type == 'clapprvideo':
                            # embed clappr video
                            record.embed_code = '<div id="externalVideo" class="clapprVideo embed-responsive-item"></div>'
                        if record.additional_type == 'localvideo':
                            # embed local video
                            #record.embed_code = '<div id="externalVideo" class="clapprVideo embed-responsive-item"></div>'
                            vals = {
                                "video/mp4": b'MPEG-4',
                                "video/webm": b'libVorbis',
                                "video/ogg": b'Ogg'
                            }
                            data = base64.b64decode(record.video_data)

                            for key, value in vals.items():
                                if data.find(value) != -1:
                                    record.mime_type = key

                            content_url = 'data:' + record.mime_type + ';base64,' + record.video_data.decode("utf-8")
                            record.embed_code = '<video class="local_video embed-responsive-item" controls controlsList="nodownload"><source src="' + content_url + '" type="' + record.mime_type + '"/></video>'
                else:
                    # embed google doc video
                    record.embed_code = '<iframe src="//drive.google.com/file/d/%s/preview" allowFullScreen="true" frameborder="0"></iframe>' % (
                        record.document_id)
            else:
                record.embed_code = False

    def _find_document_data_from_url(self, url):
        res = super(Slide, self)._find_document_data_from_url(url)
        url_obj = urls.url_parse(url)
        if url_obj.ascii_host == 'vimeo.com':
            return ('vimeo', url_obj.path[1:] if url_obj.path else False)
        if url_obj.path.find('mp4') != -1 or url_obj.path.find('mp3') != -1 or url_obj.path.find('webm') != -1 or url_obj.path.find('flv') != -1 or url_obj.path.find('ogv') != -1 or url_obj.path.find('3gp') != -1 or url_obj.path.find('m3u8') != -1 or url_obj.scheme == 'rtmp':
            return ('clapprvideo', url if url_obj.path else False)
        if url.find('localvideo-uploaded') != -1:
            return ('localvideo', 'localvideo-uploaded')
        return res

    def _parse_localvideo_document(self, document_id, only_preview_fields):
        values = {'slide_type': 'video', 'additional_type': 'localvideo', 'document_id': document_id, 'is_localvideo': True}
        return {'values': values}

    def _parse_clapprvideo_document(self, document_id, only_preview_fields):
        response = requests.get(document_id)
        if response.status_code == 404:
            return {'error': _('Please enter valid External video URL')}

        values = {'slide_type': 'video', 'additional_type': 'clapprvideo', 'document_id': document_id, 'is_localvideo': False}

        video_values = response
        if video_values:
            snippet = video_values
            if only_preview_fields:
                return values
            values.update({
                'mime_type': False,
            })
        return {'values': values}

    def _parse_vimeo_document(self, document_id, only_preview_fields):
        response = requests.get("https://vimeo.com/api/oembed.json?url=https://vimeo.com/" + document_id)
        if response.status_code == 404:
            return {'error': _('Please enter valid Vimeo URL')}

        values = {'slide_type': 'video', 'additional_type': 'vimeovideo', 'document_id': document_id,'is_localvideo': False}
        content_url = 'https://player.vimeo.com/video/' + document_id
        embed_code = '<iframe class="vimeoVideo" src="' + content_url + '" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>'

        vimeo_values = response.json()
        if vimeo_values:
            if 'title' not in vimeo_values:
                return {'error': _('Please check the privacy settings for this video before insert.')}
            snippet = vimeo_values
            if only_preview_fields:
                values.update({
                    'url_src': snippet['thumbnail_url'],
                    'title': snippet['title'],
                    'description': snippet['description']
                })
                return values
            values.update({
                'name': snippet['title'],
                'image': self._fetch_data(snippet['thumbnail_url'], {}, 'image')['values'],
                'description': snippet['description'],
                'mime_type': False,
            })
        return {'values': values}

    @api.model
    def _parse_google_document(self, document_id, only_preview_fields):
        def get_slide_type(vals):
            # TDE FIXME: WTF ??
            slide_type = 'presentation'
            if vals.get('image'):
                image = Image.open(io.BytesIO(base64.b64decode(vals['image'])))
                width, height = image.size
                if height > width:
                    return 'document'
            return slide_type

        # Google drive doesn't use a simple API key to access the data, but requires an access
        # token. However, this token is generated in module google_drive, which is not in the
        # dependencies of website_slides. We still keep the 'key' parameter just in case, but that
        # is probably useless.
        params = {}
        params['projection'] = 'BASIC'
        if 'google.drive.config' in self.env:
            access_token = self.env['google.drive.config'].get_access_token()
            if access_token:
                params['access_token'] = access_token
        if not params.get('access_token'):
            params['key'] = self.env['website'].get_current_website().website_slide_google_app_key

        fetch_res = self._fetch_data('https://www.googleapis.com/drive/v2/files/%s' % document_id, params, "json")
        if fetch_res.get('error'):
            return fetch_res

        google_values = fetch_res['values']
        if only_preview_fields:
            return {
                'url_src': google_values['thumbnailLink'],
                'title': google_values['title'],
            }

        values = {
            'name': google_values['title'],
            #'image': self._fetch_data(google_values['thumbnailLink'].replace('=s220', ''), {}, 'image')['values'],
            'mime_type': google_values['mimeType'],
            'document_id': document_id,
        }
        if google_values['mimeType'].startswith('video/'):
            values['slide_type'] = 'video'
        elif google_values['mimeType'].startswith('image/'):
            values['datas'] = values['image']
            values['slide_type'] = 'infographic'
        elif google_values['mimeType'].startswith('application/vnd.google-apps'):
            values['slide_type'] = get_slide_type(values)
            if 'exportLinks' in google_values:
                values['datas'] = \
                self._fetch_data(google_values['exportLinks']['application/pdf'], params, 'pdf', extra_params=True)[
                    'values']
                # Content indexing
                if google_values['exportLinks'].get('text/plain'):
                    values['index_content'] = \
                    self._fetch_data(google_values['exportLinks']['text/plain'], params, extra_params=True)['values']
                elif google_values['exportLinks'].get('text/csv'):
                    values['index_content'] = \
                    self._fetch_data(google_values['exportLinks']['text/csv'], params, extra_params=True)['values']
        elif google_values['mimeType'] == 'application/pdf':
            # TODO: Google Drive PDF document doesn't provide plain text transcript
            values['datas'] = self._fetch_data(google_values['webContentLink'], {}, 'pdf')['values']
            values['slide_type'] = get_slide_type(values)

        return {'values': values}

    @api.onchange('video_data')
    def _on_change_video_data(self):
        vals = {
            "video/mp4": b'MPEG-4',
            "video/webm": b'libVorbis',
            "video/ogg": b'Ogg'
        }
        if self.video_data:
            data = base64.b64decode(self.video_data)
            self.additional_type = 'localvideo'
            self.url = 'localvideo-uploaded'
            for key, value in vals.items():
                if data.find(value) != -1:
                    self.mime_type = key
            if self.additional_type == 'localvideo':
                if self.mime_type not in ["video/mp4", "video/webm", "video/ogg"]:
                    self.video_data = False
                    self.additional_type = False
                    self.url = False
                    self.is_localvideo = False
                    #self.mime_type = False
                    return {
                        'warning': {
                            'title': 'Warning!',
                            'message': 'The media file format is not supported. Please upload only mp4, ogg or webm files.'
                        }
                    }
