from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class stockMove(models.Model):
    _inherit = "stock.move"

    consolidate_id = fields.Many2one('purchase.consolidate', string='Consolidación')