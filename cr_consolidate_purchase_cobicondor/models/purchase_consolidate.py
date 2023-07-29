from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseConsolidate(models.Model):
    _name = "purchase.consolidate"

    
    name = fields.Char('Número')
    date = fields.Date('Fecha')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Confirmado'),
        ('canel', 'Cancel'),
    ], string='Estado', default = 'draft')

    line_ids = fields.One2many('purchase.consolidate.line', 'consolidate_id', string='Productos')
    purchase_ids = fields.Many2many('purchase.order', string='purchase')

    purchase_count = fields.Integer('', compute = 'set_purchase_count')

    def action_confirm(self):
        self.state = 'done'
        self.name = self.env['ir.sequence'].next_by_code('purchase.consolidate')
    
    def set_purchase_count(self):
        for rec in self:
            rec.purchase_count = len(rec.purchase_ids)
    
    def purchase_list_get(self):
        return {
            'name': 'Ordenes de compra',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'target': 'current',
            # 'res_id': self.purchase_ids.ids,
            'domain': [('id', 'in', self.purchase_ids.ids )],
        }

    
class purchaseConsolidate(models.Model):
    _name = "purchase.consolidate.line"

    
    product_id = fields.Many2one('product.product', string='Producto')
    consolidate_id = fields.Many2one('purchase.consolidate', string='Producto')
    qty = fields.Float('Cantidad')
    price_unit = fields.Float('Costo compra')

    

    