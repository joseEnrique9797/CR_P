from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseConsolidateWizard(models.TransientModel):
    _name = "purchase.consolidate.wizard"

    def get_ids_partners(self, objs):
        array = []
        for rec in objs:
            if rec.partner_id.id not in  array:
                array.append(rec.partner_id.id)
        return array
    
    def action_confirm(self):
        purchase = self.env['purchase.order'].browse(self._context.get('active_ids'))

        lines = []
        cost = 0
        for pur in purchase:
            for l in pur.order_line:
                if  l.product_qty - l.qty_received  > 0:
                    lines.append((
                        0, 0, {
                            'product_id': l.product_id.id,
                            'qty': l.product_qty - l.qty_received ,
                            'price_unit': l.price_unit,
                        },
                    ))
                    cost += l.price_unit
        # self.env['ir.sequence'].next_by_code('purchase.consolidate')
        data_partner = self.get_ids_partners(purchase)
        self.env['purchase.consolidate'].create({
            'name': 'Nuevo',
            'line_ids':lines,
            'date':datetime.now(),
            'purchase_ids':purchase.ids,
            'partner_list_ids':data_partner,
            # 'cost_total':cost,
        })
                
        

    