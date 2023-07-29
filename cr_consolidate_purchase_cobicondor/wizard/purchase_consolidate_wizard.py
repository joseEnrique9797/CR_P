from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseConsolidateWizard(models.TransientModel):
    _name = "purchase.consolidate.wizard"

    def action_confirm(self):
        purchase = self.env['purchase.order'].browse(self._context.get('active_ids'))

        lines = []

        for pur in purchase:
            for l in pur.order_line:
                lines.append((
                    0, 0, {
                        'product_id': l.product_id.id,
                        'qty': l.product_qty ,
                        'price_unit': l.price_unit,
                    },
                ))
        # self.env['ir.sequence'].next_by_code('purchase.consolidate')
        self.env['purchase.consolidate'].create({
            'name': 'Nuevo',
            'line_ids':lines,
            'date':datetime.now(),
            'purchase_ids':purchase.ids,
        })
                
        

    