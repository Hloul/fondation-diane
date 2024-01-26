from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    currency_id2 = fields.Many2one('res.currency', string='Second Currency')
