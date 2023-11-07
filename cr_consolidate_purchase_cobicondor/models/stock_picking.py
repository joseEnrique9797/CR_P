from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class stockPicking(models.Model):
    _inherit = "stock.picking"

    consolidate_id = fields.Many2one('purchase.consolidate', string='Consolidacion')
    order_consolidate_ids = fields.Many2many('purchase.order', string='Proveedores')

class stockMove(models.Model):
    _inherit = "stock.move"

    consolidate_line_id = fields.Many2one('purchase.consolidate.line', string='linea Consolidacion')

class stockMove(models.Model):
    _inherit = "account.move"

    consolidate_id = fields.Many2one('purchase.consolidate', string='Consolidacion')


