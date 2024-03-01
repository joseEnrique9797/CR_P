# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_round
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, time
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY

class resPartner(models.Model):

    _inherit = 'res.partner'

    external_id = fields.Char('ID invicta')