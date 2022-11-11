# -*- coding: utf-8 -*-

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

class Channel(models.Model):
    """ A channel is a container of slides. """
    _inherit = 'slide.channel'
    _name = 'slide.channel'

    #nbr_zoom_meeting = fields.Integer('Zoom Meeting', compute='_compute_slides_statistics', store=True)
    #nbr_externalvideo = fields.Integer('External Videos (mp4)', compute='_compute_slides_statistics', store=True)
    #nbr_googledrivevideo = fields.Integer('Google Drive Videos', compute='_compute_slides_statistics', store=True)
    #nbr_clapprvideo = fields.Integer('External Videos (livestream and other supported)', compute='_compute_slides_statistics', store=True)
    #nbr_vimeovideo = fields.Integer('Vimeo Videos', compute='_compute_slides_statistics', store=True)
    #nbr_localvideo = fields.Integer('Local Video', compute='_compute_slides_statistics', store=True)

    #@api.depends('slide_ids.slide_type', 'slide_ids.is_published', 'slide_ids.completion_time',
    #             'slide_ids.likes', 'slide_ids.dislikes', 'slide_ids.total_views', 'slide_ids.is_category',
    #             'slide_ids.active')
    #def _compute_slides_statistics(self):
    #    default_vals = dict(total_views=0, total_votes=0, total_time=0, total_slides=0)
    #    keys = ['nbr_%s' % slide_type for slide_type in
    #            self.env['slide.slide']._fields['slide_type'].get_values(self.env)]
    #    default_vals.update(dict((key, 0) for key in keys))

    #    result = dict((cid, dict(default_vals)) for cid in self.ids)
    #    read_group_res = self.env['slide.slide'].read_group(
    #        [('active', '=', True), ('is_published', '=', True), ('channel_id', 'in', self.ids),
    #         ('is_category', '=', False)],
    #        ['channel_id', 'slide_type', 'likes', 'dislikes', 'total_views', 'completion_time'],
    #        groupby=['channel_id', 'slide_type'],
    #        lazy=False)
    #    for res_group in read_group_res:
    #        cid = res_group['channel_id'][0]
    #        result[cid]['total_views'] += res_group.get('total_views', 0)
    #        result[cid]['total_votes'] += res_group.get('likes', 0)
    #        result[cid]['total_votes'] -= res_group.get('dislikes', 0)
    #        result[cid]['total_time'] += res_group.get('completion_time', 0)

    #    type_stats = self._compute_slides_statistics_type(read_group_res)
    #    for cid, cdata in type_stats.items():
    #        result[cid].update(cdata)

    #    for record in self:
    #        record.update(result.get(record.id, default_vals))

    #def _compute_slides_statistics_type(self, read_group_res):
    #    """ Compute statistics based on all existing slide types """
    #    slide_types = self.env['slide.slide']._fields['slide_type'].get_values(self.env)
    #    keys = ['nbr_%s' % slide_type for slide_type in slide_types]
    #    result = dict((cid, dict((key, 0) for key in keys + ['total_slides'])) for cid in self.ids)
    #    for res_group in read_group_res:
    #        cid = res_group['channel_id'][0]
    #        slide_type = res_group.get('slide_type')
    #        if slide_type:
    #            slide_type_count = res_group.get('__count', 0)
    #            result[cid]['nbr_%s' % slide_type] = slide_type_count
    #            result[cid]['total_slides'] += slide_type_count
    #    return result