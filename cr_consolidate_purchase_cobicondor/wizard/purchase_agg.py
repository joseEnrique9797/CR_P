from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseAgg(models.TransientModel):
    _name = "purchase.agg"

    purchase_new_ids = fields.Many2many('purchase.order', string='purchase new')

    # purchase_ids = fields.Many2many('purchase.order', string='purchase old')

    def action_confirm(self):
        consolidate = self.env['purchase.consolidate'].browse( self._context.get('active_id') )


        for line in self.purchase_new_ids:
            consolidate.write({
                'purchase_ids': [(4, line.id)]
            })

            lines = []

            for l in line.order_line:
                if  l.product_qty - l.qty_received  > 0:
                    
                    other_lines = line.env['purchase.consolidate.line'].search([
                        # ('id','!=',rec.id),
                        ('state','=','pending'),
                        ('purchase_line_id','=',line.id),
                        ('product_id','=',l.product_id.id),
                    ])
        
                    total = sum(x.qty_transito for x in other_lines)
                    
                    qty_available_before_transito = (l.product_qty - l.qty_received) - total
                    
                    
                    # lines.append((
                    #     0, 0, {
                    #         'product_id': l.product_id.id,
                    #         'purchase_line_id': line.id,
                    #         'purchase_line_data_id': l.id,
                    #         'qty': l.product_qty - l.qty_received ,
                    #         'qty_available_before_transito': qty_available_before_transito ,
                    #         'qty_transito': qty_available_before_transito ,
                    #         'price_unit': l.price_unit,
                    #         'consolidate_id':consolidate.id
                    #     },
                    # ))

                    lines.append({
                            'product_id': l.product_id.id,
                            'purchase_line_id': line.id,
                            'purchase_line_data_id': l.id,
                            'qty': l.product_qty - l.qty_received ,
                            'qty_available_before_transito': qty_available_before_transito ,
                            'qty_transito': qty_available_before_transito ,
                            'price_unit': l.price_unit,
                            'consolidate_id':consolidate.id
                        }
                    )
                    # cost += l.price_unit
                        
                line.consolidate_apply = True
            self.env['purchase.consolidate.line'].create(lines)
