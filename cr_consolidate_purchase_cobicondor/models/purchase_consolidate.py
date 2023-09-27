from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class purchaseConsolidate(models.Model):
    _name = "purchase.consolidate"

    
    name = fields.Char('Número')
    num_emb = fields.Char('Número de embarque')
    date = fields.Date('Fecha')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('transit', 'En transito'),
        ('pending', 'Recibido'),
        ('done', 'Confirmado'),
        ('cancel', 'Cancelado'),
    ], string='Estado', default = 'draft')

    line_ids = fields.One2many('purchase.consolidate.line', 'consolidate_id', string='Productos')
    purchase_ids = fields.Many2many('purchase.order', string='purchase')
    
    partner_list_ids = fields.Many2many('res.partner', string='Proveedores')

    purchase_count = fields.Integer('', compute = 'set_purchase_count')
    currency_id = fields.Many2one('res.currency', string='Moneda', compute = 'set_company_currency_id')
    cost_total = fields.Monetary('Costo total', compute = 'set_cost_total_consolidate')

    def action_cancel(self):
        self.state = 'cancel'
    
    @api.depends('line_ids')
    def set_cost_total_consolidate(self):
        for rec in self:
            total = 0
            for line in rec.line_ids:
                total += line.cost_subtotal
            rec.cost_total = total
            
    
    def unlink(self):
        for rec in self:
           if rec.state != 'draft':
               raise ValidationError("No se puede borrar una consolidacion en estado confirmado")
        return super(purchaseConsolidate,self).unlink()

    def set_company_currency_id(self):
        for rec in self:
            # company = self.env['res.company'].search([
            #     ('id','>',0)
            # ], limit = 1)

            currency = self.env['res.currency'].search([
                ('name', '=', 'USD'),
                ('symbol', '=', '$'),
            ])

            rec.currency_id = currency.id if currency else False
            
    
    def action_confirm(self):
        self.state = 'transit'
        self.name = self.env['ir.sequence'].next_by_code('purchase.consolidate')

    def action_pending(self):
        self.state = 'pending'
        # self.name = self.env['ir.sequence'].next_by_code('purchase.consolidate')
    

    def action_confirm_dos(self):
        self.state = 'done'
    
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

    
class purchaseConsolidateLine(models.Model):
    _name = "purchase.consolidate.line"


    name = fields.Char('Número', related = 'consolidate_id.name' )
    num_emb = fields.Char('Número de embarque', related = 'consolidate_id.num_emb', store=True)
    date = fields.Date('Fecha', related = 'consolidate_id.date')

    
    purchase_line_id = fields.Many2one('purchase.order', string='purchase')
    purchase_line_data_id = fields.Many2one('purchase.order.line', string='purchase')
    product_id = fields.Many2one('product.product', string='Producto')
    consolidate_id = fields.Many2one('purchase.consolidate', string='Producto')
    
    qty = fields.Float('Comprado', related = 'purchase_line_data_id.product_qty')
    qty_transito = fields.Float('En transito')
    qty_received = fields.Float('Recibido', related = 'purchase_line_data_id.qty_received')
    qty_restant = fields.Float('Pendiente', compute = 'set_qty_restant')

    
    price_unit = fields.Float('Costo unitario')
    cost_subtotal = fields.Float('Costo compra', compute = 'set_cost_subtotal')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Confirmado'),
        ('canel', 'Cancel'),
    ], string='Estado', default = 'draft', related = 'consolidate_id.state')

    @api.onchange('qty_transito')
    def onchange_qty_transito(self):
        for rec in self:
            if rec.qty_transito > rec.qty :
                raise ValidationError("La cantidad en transito no puede ser mayor a la cantidad comprada.") 
    
    @api.depends('qty_received','qty')
    def set_qty_restant(self):
        for rec in self:
            rec.qty_restant = rec.qty - rec.qty_received 
    
    @api.depends('price_unit','qty')
    def set_cost_subtotal(self):
        for rec in self:
            rec.cost_subtotal = rec.price_unit * rec.qty
    
    def action_desp_set(self):
        if self.qty_received >= self.qty_transito:
            raise ValidationError("Ya no puede recibir más productos desde esta consolidación, ya que se alcanzó la cantidad máxima definida en tránsito.") 
        # return {
        #     'name': 'Recepción',
        #     'view_mode': 'list,form',
        #     'res_model': 'stock.picking',
        #     'type': 'ir.actions.act_window',
        #     'target': 'current',
        #     # 'res_id': self.purchase_ids.ids,
        #     'domain': [('purchase_id', '=', self.purchase_line_id.id )],
        # }
        # pass
        vendors = self.env['stock.location'].search([
            ('name', '=', 'Vendors')
        ], limit = 1)
        
        stock = self.env['stock.picking.type'].search([
            ('name', '=', 'Recepciones')
        ], limit = 1)
        
        location_dest_id = self.env['stock.location'].search([
            ('name', '=', 'Stock')
        ], limit = 1)
        
        # uom_uom = self.env['uom.uom'].search([
        #     ('name', '=', 'Unidad')
        # ], limit = 1)  
        
        # if not uom_uom:
        #     uom_uom = self.env['uom.uom'].search([
        #         ('name', '=', 'Unidades')
        #     ], limit = 1) 
        
        if not stock or not location_dest_id:
            raise UserError('Configure una transferencia de tipo recepción o Stock')
        
        
        
        lines = []
        lines.append( (0,0,{
            'name':'Borrador', 
            'product_id':self.product_id.id, 
            'product_uom_qty':self.qty_transito,
            'product_uom':self.product_id.uom_id.id,
        }) )
        
        vals = {
            'picking_type_id': stock.id,
            'location_id': vendors.id,
            'location_dest_id': location_dest_id.id,
            'move_ids_without_package': lines,
        }
        
        obj = self.env['stock.picking'].create(vals)
        return {
            'name': 'Recepción',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', '=', obj.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
 

    

    