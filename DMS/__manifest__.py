# -*- coding: utf-8 -*-
{
    'name': "DMS",

    'summary': "Document Management",

    'description': """
        App to upload and manage your documents.
    """,

    'author': "BAS",
    'category': 'Extra Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal', 'web','project','documents'],

    # always loaded
    'data': [
        'views/documentmanagementview.xml',
        'demo/data.xml',
        'security/ir.model.access.csv'
    ],

}
