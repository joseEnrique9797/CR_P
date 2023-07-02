from odoo import api, fields, models
import random
import string

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    # notify_to = fields.Char(string='Notificar estado de cuenta', config_parameter='cr_financial_statement_report.notify_to',)
    accounts_report_statement = fields.Text('Cuentas por Cobrar', config_parameter='cr_financial_statement_report.accounts_report_statement')