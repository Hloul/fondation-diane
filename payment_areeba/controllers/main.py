# -*- coding: utf-8 -*-
import pprint
import logging
from werkzeug import utils

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class AreebaController(http.Controller):

    @http.route('/payment/areeba/return/<string:order_id>', type='http', auth='public', csrf=False)
    def areeba_return(self, order_id, **post):
        request.env['payment.transaction'].sudo().form_feedback(order_id, 'areeba')
        return utils.redirect("/payment/process")

    @http.route('/payment/areeba/cancel/<string:order_id>', type='http', auth="public", csrf=False)
    def areeba_cancel(self, order_id, **post):
        txn = request.env['payment.transaction'].sudo().search([('reference', '=', order_id)])
        if txn:
            txn._set_transaction_cancel()
        """ When the user cancels its Areeba payment: GET on this route """
        _logger.info('Beginning Areeba cancel with post data %s', pprint.pformat(post))
        return utils.redirect('/payment/process')
