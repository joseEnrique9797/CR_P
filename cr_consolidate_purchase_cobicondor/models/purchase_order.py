from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseOrder(models.Model):
    _inherit = "purchase.order"


    consolidate_apply = fields.Boolean(string="Documento consolidado", default = False)
    # state = fields.Selection(
    #     selection_add=[
    #         ("consolidate", "Consolidado"),
    #     ],
    # )