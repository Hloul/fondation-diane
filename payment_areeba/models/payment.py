# coding: utf-8

import json
import logging
import pprint
import requests

from werkzeug import urls

from odoo import api, fields, models

from odoo.addons.payment import utils as payment_utils
from odoo.exceptions import ValidationError

from odoo.tools.float_utils import float_compare


_logger = logging.getLogger(__name__)


class AcquirerAreeba(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('areeba', 'Areeba')])
    areeba_merchant_id = fields.Char('Areeba Merchant id', required_if_provider='areeba', groups='base.group_user')
    areeba_api_password = fields.Char('Areeba Api Password', required_if_provider='areeba', groups='base.group_user')
    areeba_payment_logo = fields.Binary(groups='base.group_user')

    def _areeba_request(self, url, data=False, method="POST"):
        self.ensure_one()
        headers = {
            'Content-Type': 'application/json'
        }
        auth = ('merchant.%s' % self.areeba_merchant_id, self.areeba_api_password)
        resp = requests.request(method, url, auth=auth, data=json.dumps(data) if data else False, headers=headers)
        # import pdb;pdb.set_trace()
        resp.raise_for_status()
        return resp.json()

    @api.multi
    def areeba_form_generate_values(self, values):
        base_url = self.get_base_url()
        areeba_tx_values = dict(values)
        url = 'https://ap-gateway.mastercard.com/api/rest/version/60/merchant/%s/session' % self.areeba_merchant_id
        url = 'https://ap-gateway.mastercard.com/api/rest/version/60/merchant/%s/session' % self.areeba_merchant_id
        data = {
            "apiOperation": "CREATE_CHECKOUT_SESSION",
            "interaction": {
                "operation": "PURCHASE",
                "returnUrl": urls.url_join(base_url, '/payment/areeba/return/%s' % values['reference']),
                "cancelUrl": urls.url_join(base_url, '/payment/areeba/cancel/%s' % values['reference']),
                "displayControl": {
                    "customerEmail": "OPTIONAL",
                },
            },
            "order": {
                "currency": values['currency'].name,
                "id": values['reference'],
                "amount": values['amount']
            },
            "customer": {
                "email": values.get('billing_partner_email'),
            },
            "userId": values.get('billing_partner_id')
        }
        resp_data = self._areeba_request(url, data)
        areeba_tx_values.update({
            'merchant_id': self.areeba_merchant_id,
            'session_id': resp_data.get('session', {}).get('id'),
            'currency': values['currency'].name,
            'merchant_name': self.company_id.name,
            'merchant_street': self.company_id.street,
            'merchant_street_2': self.company_id.street2,
        })
        if self.areeba_payment_logo:
            # test_base_url = "https://localhost:8069/"
            areeba_tx_values['logo'] = urls.url_join(base_url, 'web/image/%s/%s/areeba_payment_logo' % (self._name, self.id))

        return areeba_tx_values


class TxAreeba(models.Model):
    _inherit = 'payment.transaction'

    def form_feedback(self, data, acquirer_name):
        if data and acquirer_name == "areeba":
            txs = self.search([('reference', '=', data)])
            if not txs or len(txs) > 1:
                error_msg = 'Areeba: received data for reference %s' % (data)
                if not txs:
                    error_msg += '; no order found'
                else:
                    error_msg += '; multiple order found'
                _logger.info(error_msg)
                raise ValidationError(error_msg)
            acquirer = txs.acquirer_id
            url = 'https://ap-gateway.mastercard.com/api/rest/version/60/merchant/%s/order/%s' % (acquirer.areeba_merchant_id, data)
            data = acquirer._areeba_request(url, method="GET")
            _logger.info(
                "Areeba: entering form_feedback with post data %s"
                % pprint.pformat(data)
            )
            data['payment_transaction'] = txs
        return super(TxAreeba, self).form_feedback(data, acquirer_name)

    @api.model
    def _areeba_form_get_tx_from_data(self, data):
        return data['payment_transaction']

    @api.multi
    def _areeba_form_get_invalid_parameters(self, data):
        invalid_parameters = []

        if data.get('currency') != self.currency_id.name:
            invalid_parameters.append(('currency', data.get('currency'), self.currency_id.name))
        if float_compare(float(data.get('amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('amount'), '%.2f' % self.amount))
        if data.get('merchant') != self.acquirer_id.areeba_merchant_id:
            invalid_parameters.append(('merchant', data.get('merchant'), self.acquirer_id.areeba_merchant_id))

        return invalid_parameters

    @api.multi
    def _areeba_form_validate(self, data):
        status = data.get('result')
        former_tx_state = self.state
        res = {
            'acquirer_reference': data.get('id')
        }
        if status == 'SUCCESS':
            self._set_transaction_done()
            if self.state == 'done' and self.state != former_tx_state:
                email = data.get('customer', {}).get('email')
                if email:
                    if data.get('transaction')[0].get('userId'):
                        user_id = int(data.get('transaction')[0].get('userId'))
                    if data.get('transaction')[1].get('userId'):
                        user_id = int(data.get('transaction')[1].get('userId'))
                    billing_partner_id = data.get('transaction') and user_id
                    billing_partner = self.env['res.partner'].browse(billing_partner_id)
                    if billing_partner.exists() and email != billing_partner.email:
                        billing_partner.email = email
                _logger.info('Validated Areeba payment for tx %s: set as done' % (self.reference))
                return self.write(res)
            return True
        elif status == 'PENDING':
            self._set_transaction_pending()
            return self.write(res)
        else:
            error = 'Received unrecognized status for Areeba payment %s: %s, set as error' % (self.reference, status)
            res.update(state_message=error)
            self._set_transaction_cancel()
            if self.state == 'cancel' and self.state != former_tx_state:
                _logger.info(error)
                return self.write(res)
            return True
