# -*- coding: utf-8 -*-

{
    "name": "Website Show Popup (Website Popup)",
    "summary": "This module helps you to Show Popup Message while load odoo website pages",
    "description": """This module helps you to Show Popup Message while load odoo website pages""",
    "author": "Ananthu Krishna",
    "maintainer": "Ananthu Krishna",
    "license": "Other proprietary",
    "website": "http://www.codersfort.com",
    "images": [],
    "category": "Website",
    "depends": ['website'],
    "data": [
        'views/website_views.xml',
        'views/website_templates.xml',
    ],
    "installable": True,
    "application": True,
    "price": 15,
    "currency": "EUR",
    'assets': {
        'web.assets_frontend': [
            '/website_show_popup/static/src/js/website_show_popup.js',
        ],
    },
}
