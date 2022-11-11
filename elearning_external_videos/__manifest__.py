# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'External and Local Videos - WebSite Slides',
    'version': '1.5',
    'summary': 'Manage and publish local and external videos in website_slides',
    'category': 'Website/Website',
    'description': """
Insert external videos
======================

Features
 * External Videos: MP4, HLS, WEBM, OGG, 3GP
 * Livestreaming origin (M3U8, RTMP)
 * Support Google Drive Videos
 * Support Vimeo Videos
 * Support local uploaded Videos (mp4, ogg and webm)
""",
    'author': 'Josue Rodriguez - GAMA Recursos Tecnologicos (PERU)',
    'website': 'https://www.recursostecnologicos.pe',
    'depends': ['website_slides'],
    'data': [
        'views/loadjs.xml',
        'views/website_slides.xml',
        'views/slide_slide.xml',
        ],
    'demo': [
     ],
    'test': [],
    'images': ['images/main_screenshot.png','images/main_1.png', 'images/main_2.png'],
    'installable': True,
    'auto_install': True,
    'application': True,
    'price': 35.00,
    'currency': 'EUR',
    'license': 'OPL-1',
    'support': 'info@recursostecnologicos.pe',
    #'post_init_hook': 'post_init',
}
