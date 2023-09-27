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
            # if pur.invoice_status != 'to invoice':
            #    raise ValidationError("No se puede consolidar pedidos de compra que no esten en estado para facturar (%s)" %(pur.name))
            for l in pur.order_line:
                if  l.product_qty - l.qty_received  > 0:
                    lines.append((
                        0, 0, {
                            'product_id': l.product_id.id,
                            'purchase_line_id': pur.id,
                            'purchase_line_data_id': l.id,
                            'qty': l.product_qty - l.qty_received ,
                            'qty_transito': l.product_qty - l.qty_received ,
                            'price_unit': l.price_unit,
                        },
                    ))
                    cost += l.price_unit
            
            pur.consolidate_apply = True
            # raise ValidationError("== 11111 =======>%s " %(pur.consolidate_apply)) 
            # pur.consolidate_apply = True
        # self.env['ir.sequence'].next_by_code('purchase.consolidate')
        data_partner = self.get_ids_partners(purchase)
        create_obj = self.env['purchase.consolidate'].create({
            'name': 'Nuevo',
            'line_ids':lines,
            'date':datetime.now(),
            'purchase_ids':purchase.ids,
            'partner_list_ids':data_partner,
            # 'cost_total':cost,
        })

        return {
            'name': 'Consolidación',
            'view_mode': 'list,form',
            'res_model': 'purchase.consolidate',
            'type': 'ir.actions.act_window',
            'target': 'current',
            # 'res_id': self.purchase_ids.ids,
            'domain': [('id', '=', create_obj.id )],
        }
                
        

    