# -*- coding: utf-8 -*-
# updated code by kishan for a payment
{
    'name': 'Areeba Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: Areeba Implementation',
    'version': '1.0.0.2',
    'description': """Areeba Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_areeba_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
