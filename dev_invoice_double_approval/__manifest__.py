# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Invoice double approval workflow',
    'version': '12.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Accounting',
    'description':
        """
       This odoo Module add Invoice double approval workflow functionality into odoo

        1.Set limit on Invoices, So, Manager must have confirm Invoice if it exceed the Pre-Defined Limit.
        2.Specify customer and supplier invoice limit separately.
        3.If invoice amount exceeds pre-defined limit then it will send confirmation emails
        
         Invoice Double Approval, Double Approval, Approval Process, Invoice Approval,  Invoice Approval workflow , Approval Invoice, two lavel process, two way approval, Invoice validatataion, Invoice two step validatataion
Invoice double approval workflow
Oddo Invoice double approval workflow
Incoice approval workflow
Odoo invoice approval workflow
Invoice double approval 
Odoo invoice double approval
Odoo apps Invoice double approval process workflow
Odoo  Invoice double approval process workflow
Set limit on Invoices
Odoo Set limit on Invoices
Invoice limit 
Odoo invoice limit
Invoice approval 
Odoo invoice approval
Check invoice approval 
Odoo check invoice approval
    """,
    'summary': 'odoo app Allow you to Double Approval process Workflow into Invoice',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['base', 'account'],
    'data': [
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/account_invoice_view.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':29.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
