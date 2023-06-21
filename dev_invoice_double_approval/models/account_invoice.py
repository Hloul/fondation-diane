# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    state = fields.Selection([('draft','Draft'),
                              ('open', 'Open'),
                              ('to approve', 'To Approve'),
                              ('in_payment', 'In Payment'),
                              ('paid', 'Paid'),
                              ('cancel', 'Cancelled'),],
                             string='Status', index=True, readonly=True,
                             default='draft', track_visibility='onchange',
                             copy=False,
                             help=
                             " * The 'Draft' status is used when a user is "
                             "encoding a new and unconfirmed Invoice.\n * The "
                             "'Open' status is used when user creates invoice,"
                             " an invoice number is generated. It stays in the"
                             " open status till the user pays the invoice.\n *"
                             " The 'In Payment' status is used when payments "
                             "have been registered for the entirety of the "
                             "invoice in a journal configured to post entries"
                             " at bank reconciliation only, and some of them"
                             " haven't been reconciled with a bank statement "
                             "line yet.\n * The 'Paid' status is set "
                             "automatically when the invoice is paid. Its "
                             "related journal entries may or may not be"
                             " reconciled.\n * The 'Cancelled' status is "
                             "used when user cancel invoice.")

    @api.multi
    def _make_url(self, record_id, model_name, menu_id, action_id):
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url')
        if base_url:
            base_url += \
                '/web?#id=%s&action=%s&model=%s&view_type=form&menu_id=%s' \
                % (record_id, action_id, model_name, menu_id)
        return base_url

    @api.multi
    def action_invoice_open(self):
        for invoice in self:
            if invoice.state not in ['draft']:
                continue
            if invoice.type == 'out_invoice':
                ir_param = invoice.env['ir.config_parameter'].sudo()
                is_double_enabled = \
                    bool(ir_param.get_param(
                        'dev_invoice_double_approval.double_verify'))
                if is_double_enabled:
                    validation_amount = \
                        float(ir_param.get_param(
                            'dev_invoice_double_approval.'
                            'customer_invoice_double_validation_amount'))
                    user_has_approval_right = \
                        self.env.user.has_group(
                            'dev_invoice_double_approval.'
                            'double_verification_invoice_right')
                    if invoice.amount_total < validation_amount \
                            or user_has_approval_right:
                        return super(AccountInvoice, self).action_invoice_open()
                    else:
                        authorized_group = \
                            self.env.ref('dev_invoice_double_approval.'
                                         'double_verification_invoice_right')
                        authorized_users = self.env['res.users'].\
                            search([('groups_id', '=', authorized_group.id)])
                        menu_id = \
                            self.env.ref('account.menu_action_invoice_tree1').id
                        action_id = \
                            self.env.ref('account.action_invoice_tree1').id
                        invoice_url =\
                            self._make_url(invoice.id, invoice._name,
                                           menu_id, action_id)
                        if authorized_users:
                            for au_user in authorized_users:
                                email_body = ''' <span style='font-style: 16px;
                                 font-weight: bold;'>Dear, %s</span>
                                  ''' % ( au_user.name) + '''
                                   <br/><br/>''' + ''' <span style='font-style:
                                    14px;'> An Invoice from <span
                                     style='font-weight: bold;'>%s</span> is
                                     awaiting for your Approval to be Validated
                                     </span>''' % (self.env.user.name) + '''
                                      <br/>''' + '''<span style='font-style:
                                      14px;'>Please, access it form below
                                      button</span>
                                      <div style="margin-top:40px;"> <a href=
                                      "''' + invoice_url + '''"
                                      style="background-color: #1abc9c;
                                      padding: 20px; text-decoration: none;
                                       color: #fff; border-radius: 5px;
                                       font-size: 16px;
                                       "class="o_default_snippet_text">
                                       View Invoice</a></div><br/><br/>'''
                                email_id = \
                                    self.env['mail.mail'].\
                                        create(
                                        {'subject': 'Customer Invoice is '
                                                    'Waiting for Approval',
                                         'email_from':
                                             self.env.user.partner_id.email,
                                         'email_to': au_user.partner_id.email,
                                         'message_type': 'email',
                                         'body_html': email_body,
                                         })
                                email_id.send()
                        invoice.write({'state': 'to approve'})
                else:
                    return super(AccountInvoice, self).action_invoice_open()
            if invoice.type == 'in_invoice':
                ir_param = invoice.env['ir.config_parameter'].sudo()
                is_double_enabled = bool(ir_param.get_param(
                    'dev_invoice_double_approval.double_verify'))
                if is_double_enabled:
                    validation_amount = \
                        float(ir_param.get_param(
                            'dev_invoice_double_approval.'
                            'supplier_invoice_double_validation_amount'))
                    user_has_approval_right = \
                        self.env.user.has_group(
                            'dev_invoice_double_approval.'
                            'double_verification_invoice_right')
                    if invoice.amount_total < validation_amount \
                            or user_has_approval_right:
                        return super(AccountInvoice, self).action_invoice_open()
                    else:
                        authorized_group = \
                            self.env.ref('dev_invoice_double_approval.'
                                         'double_verification_invoice_right')
                        authorized_users = self.env['res.users'].\
                            search([('groups_id', '=', authorized_group.id)])
                        menu_id = \
                            self.env.ref('account.menu_action_invoice_tree2').id
                        action_id = \
                            self.env.ref('account.action_invoice_tree2').id
                        invoice_url = \
                            self._make_url(invoice.id, invoice._name,
                                           menu_id, action_id)
                        if authorized_users:
                            for au_user in authorized_users:
                                email_body = ''' <span style='font-style: 16px;
                                 font-weight: bold;'>Dear, %s</span>
                                  ''' % ( au_user.name) + '''
                                   <br/><br/>''' + ''' <span style='font-style:
                                    14px;'> A Bill from <span
                                     style='font-weight: bold;'>%s</span> is
                                     awaiting for your Approval to be Validated
                                     </span>''' % (self.env.user.name) + '''
                                      <br/>''' + '''<span style='font-style:
                                      14px;'>Please, access it form below
                                      button</span>
                                      <div style="margin-top:40px;"> <a href=
                                      "''' + invoice_url + '''"
                                      style="background-color: #1abc9c;
                                      padding: 20px; text-decoration: none;
                                       color: #fff; border-radius: 5px;
                                       font-size: 16px;
                                       "class="o_default_snippet_text">
                                       View Bill</a></div><br/><br/>'''
                                email_id = \
                                    self.env['mail.mail'].\
                                        create(
                                        {'subject': 'Vendor Bill is Waiting for'
                                                    ' Approval',
                                         'email_from':
                                             self.env.user.partner_id.email,
                                         'email_to': au_user.partner_id.email,
                                         'message_type': 'email',
                                         'body_html': email_body,
                                         })
                                email_id.send()
                        invoice.write({'state': 'to approve'})
                else:
                    return super(AccountInvoice, self).action_invoice_open()
            if invoice.type not in ['out_invoice', 'in_invoice']:
                return super(AccountInvoice, self).action_invoice_open()

    @api.multi
    def make_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: not inv.partner_id):
            raise UserError(_("The field Vendor is required, please complete it"
                              " to validate the Vendor Bill."))
        if to_open_invoices.filtered(lambda inv: float_compare(
                inv.amount_total, 0.0,
                precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative"
                              " total amount. You should create a credit "
                              "note instead."))
        if to_open_invoices.filtered(lambda inv: not inv.account_id):
            raise UserError(_('No account was found to create the invoice, be'
                              ' sure you have installed a chart of account.'))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()

    @api.multi
    def make_invoice_cancel(self):
        for invoice in self:
            return invoice.action_cancel()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: