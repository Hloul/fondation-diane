from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency_id2 = fields.Many2one(string='Second Company Currency', related='company_id.currency_id2',
                                          readonly=True)
    computed_rate = fields.Float(string='Computed Rate', compute='_compute_conversion_rate', inverse='_inverse_conversion_rate')
    conversion_rate = fields.Float(string='Conversion Rate', default=0, store=True)
    debit2 = fields.Monetary(string='Debit2', currency_field='company_currency_id2', default=0)
    credit2 = fields.Monetary(string='Credit2', currency_field='company_currency_id2', default=0)

    @api.depends('amount_currency','date','currency_id','debit','credit')
    def _compute_conversion_rate(self):
        for rec in self:
          _logger.info('MC: b4 conversion_rate %s', rec.conversion_rate)
          #if rec.conversion_rate == 0:
            rec.debit2 = 0
            rec.credit2 = 0
            rec.conversion_rate = 1
            if rec.debit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                main_currency = self.env.company.currency_id
                from_currency = rec.currency_id
                to_currency = self.env.company.currency_id2
                if from_currency.id == to_currency.id:
                    conversion_rate = rec.debit / abs(rec.amount_currency)
                    rec.debit2 = abs(rec.amount_currency)
                    _logger.info('MC: from==to debit2 %s', rec.debit2)
                    _logger.info('MC: from==to conversion_rate %s', conversion_rate)
                else:
                    if rec.move_id.asset_id:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                        )
                        rec.debit2 = rec.debit / conversion_rate
                    else:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            to_currency, main_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.debit2 = rec.debit / conversion_rate
                        _logger.info('MC: from<>to debit2 %s', rec.debit2)
                        _logger.info('MC: from<>to conversion_rate %s', conversion_rate)
                #rec.conversion_rate = conversion_rate
            if rec.credit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                main_currency = self.env.company.currency_id
                from_currency = rec.currency_id
                to_currency = self.env.company.currency_id2
                if from_currency.id == to_currency.id:
                    conversion_rate = rec.credit / abs(rec.amount_currency)
                    rec.credit2 = abs(rec.amount_currency)
                    _logger.info('MC: from==to credit2 %s', rec.credit2)
                    _logger.info('MC: from==to conversion_rate %s', conversion_rate)
                else:
                    if rec.move_id.asset_id:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                        )
                        rec.credit2 = rec.credit / conversion_rate
                    else:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            to_currency, main_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.credit2 = rec.credit / conversion_rate
                        _logger.info('MC: from<>to credit2 %s', rec.credit2)
                        _logger.info('MC: from==to conversion_rate %s', conversion_rate)
                #rec.conversion_rate = conversion_rate
            rec.computed_rate = conversion_rate
            _logger.info('MC: end new calc rec.computed_rate %s', rec.computed_rate)
          #else:
            #conversion_rate = rec.conversion_rate
            #rec.debit2 = rec.debit / conversion_rate
            #rec.credit2 = rec.credit / conversion_rate
            #rec.computed_rate = conversion_rate
            #_logger.info('MC: no calc conversion_rate %s', conversion_rate)
            #_logger.info('MC: no calc debit2 %s', rec.debit2)
            #_logger.info('MC: no calc credit2 %s', rec.credit2)

    def _inverse_conversion_rate(self):
        for rec in self:
          conversion_rate = rec.computed_rate
          rec.debit2 = rec.debit / conversion_rate
          rec.credit2 = rec.credit / conversion_rate
          _logger.info('MC inverse: conversion_rate %s', computed_rate)
          _logger.info('MC inverse: debit2 %s', rec.debit2)
          _logger.info('MC inverse: credit2 %s', rec.credit2)
          

