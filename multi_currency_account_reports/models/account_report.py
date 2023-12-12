from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountReport(models.Model):
    _inherit = 'account.report'

    def _caret_options_initializer_default(self):
        res = super(AccountReport, self)._caret_options_initializer_default()
        res['account.account'].append(
            {'name': _("Multi Currency General Ledger"), 'action': 'caret_option_open_general_ledger_multi_currency'},
        )
        return res

    def caret_option_open_general_ledger_multi_currency(self, options, params):
        model, record_id = self._get_model_info_from_id(params['line_id'])

        if model != 'account.account':
            raise UserError(_("'Open General Ledger' caret option is only available form report lines targetting accounts."))

        account_line_id = self._get_generic_line_id('account.account', record_id)
        gl_options = self.env.ref('multi_currency_account_reports.general_ledger_multi_currency_report')._get_options(options)
        gl_options['unfolded_lines'] = [account_line_id]

        action_vals = self.env['ir.actions.actions']._for_xml_id('multi_currency_account_reports.action_account_report_general_ledger_multi_currency')
        action_vals['params'] = {
            'options': gl_options,
            'ignore_session': 'read',
        }

        return action_vals

    def _get_partner_and_general_ledger_initial_balance_line(self, options, parent_line_id, eval_dict, account_currency=None):
        """ Helper to generate dynamic 'initial balance' lines, used by general ledger and partner ledger.
        """
        line_columns = []
        for column in options['columns']:
            col_value = eval_dict[column['column_group_key']].get(column['expression_label'])
            col_expr_label = column['expression_label']

            if col_value is None or (col_expr_label == 'amount_currency' and not account_currency):
                line_columns.append({})
            else:
                if col_expr_label == 'amount_currency':
                    formatted_value = self.format_value(col_value, currency=account_currency, figure_type=column['figure_type'])
                elif col_expr_label in ['debit2', 'credit2']:
                    formatted_value = self.format_value(col_value, currency=self.env.company.currency_id2, figure_type=column['figure_type'])
                else:
                    formatted_value = self.format_value(col_value, figure_type=column['figure_type'])

                line_columns.append({
                    'name': formatted_value,
                    'no_format': col_value,
                    'class': 'number',
                })

        if not any(column.get('no_format') for column in line_columns):
            return None

        return {
            'id': self._get_generic_line_id(None, None, parent_line_id=parent_line_id, markup='initial'),
            'class': 'o_account_reports_initial_balance',
            'name': _("Initial Balance"),
            'parent_id': parent_line_id,
            'columns': line_columns,
        }

