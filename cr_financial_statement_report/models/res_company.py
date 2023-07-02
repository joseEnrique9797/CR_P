# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from datetime import datetime
# from datetime import timedelta

class resCompany(models.Model):
    _inherit = 'res.company'

    # notifi_account_report = fields.Text('Cuentas a notificar')
    notifi_account_report = fields.Html('Notificar pólizas sin renovar a')