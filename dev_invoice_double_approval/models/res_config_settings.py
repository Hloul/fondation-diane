# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    double_verify = fields.Boolean(string="Double Approval")
    customer_invoice_double_validation_amount \
        = fields.Float(string="Customer Invoice Minimum Amount")
    supplier_invoice_double_validation_amount \
        = fields.Float(string="Supplier Invoice Minimum Amount")

    @api.model
    def set_values(self):
        ir_param = self.env['ir.config_parameter'].sudo()
        ir_param.set_param('dev_invoice_double_approval.double_verify',
                           self.double_verify)
        ir_param.set_param('dev_invoice_double_approval.'
                           'customer_invoice_double_validation_amount',
                           self.customer_invoice_double_validation_amount)
        ir_param.set_param('dev_invoice_double_approval.'
                           'supplier_invoice_double_validation_amount',
                           self.supplier_invoice_double_validation_amount)
        super(ResConfigSettings, self).set_values()


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_param = self.env['ir.config_parameter'].sudo()
        double_verify = \
            ir_param.get_param('dev_invoice_double_approval.double_verify')
        customer_invoice_double_validation_amount \
            = ir_param.get_param('dev_invoice_double_approval.'
                                 'customer_invoice_double_validation_amount')
        supplier_invoice_double_validation_amount \
            = ir_param.get_param('dev_invoice_double_approval.'
                                 'supplier_invoice_double_validation_amount')
        res.update(
            double_verify=bool(double_verify),
            customer_invoice_double_validation_amount=
            float( customer_invoice_double_validation_amount),
            supplier_invoice_double_validation_amount=
            float( supplier_invoice_double_validation_amount),
        )
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: