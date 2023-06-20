from odoo import _, api, fields, models, tools
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class stockMoveLine(models.Model):
    _inherit = 'stock.move'
    
    qty_received = fields.Float('Recibido')
    
#     @api.depends('qty_received')
#     def depends_qty_received(self):
#         raise UserError('depends_qty_received=========****========> %s' %(self.id))
#         self.picking_id.date_desp = datetime.now()
#         self.picking_id.user_desp_id = self.env.user.id
        
#         # self.picking_id.write({
#         #     'date_desp':datetime.now(),
#         #     'user_desp_id':self.env.user.id,
#         # })
        
#     @api.onchange('qty_received')
#     def onchange_qty_received(self):
#         # print(op2222)
#         raise UserError('onchange_qty_received=================> %s' %(self))
#         self.picking_id.date_desp = datetime.now()
#         self.picking_id.user_desp_id = self.env.user.id
        
#         self.picking_id.write({
#             'date_desp':datetime.now(),
#             'user_desp_id':self.env.user.id,
#         })
    
class stockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    qty_received = fields.Float('Recibido')
    
#     @api.depends('qty_received')
#     def depends_qty_received(self):
#         raise UserError('depends_qty_received =================> %s' %(self.id))
#         self.picking_id.date_desp = datetime.now()
#         self.picking_id.user_desp_id = self.env.user.id
#         # print(op55)
#         # self.picking_id.write({
#         #     'date_desp':datetime.now(),
#         #     'user_desp_id':self.env.user.id,
#         # })
        
#     @api.onchange('qty_received')
#     def onchange_qty_received(self):
#         # print(op1111)
#         raise UserError('onchange_qty_received =================> %s' %(self))
#         self.picking_id.date_desp = datetime.now()
#         self.picking_id.user_desp_id = self.env.user.id
#         self.picking_id.write({
#             'date_desp':datetime.now(),
#             'user_desp_id':self.env.user.id,
#         })
        

class stockPicking(models.Model):
    _inherit = 'stock.picking'
    
    cost_id = fields.Many2one('job.cost.sheet', string='Requisicion')
    
    user_desp_id = fields.Many2one('res.users', string='Recibido por', copy=False)
    date_desp = fields.Datetime('Fecha de Recepción', copy=False)
    
    
#     @api.depends('move_line_ids_without_package.qty_received', 'move_ids_without_package.qty_received')
#     def depends_qty_received(self):
        
#         # print(op2222)
        
#         raise UserError('test 2222222222222222=================> %s' %(self))
        
#         self.picking_id.date_desp = datetime.now()
#         self.picking_id.user_desp_id = self.env.user.id
        
#         self.picking_id.write({
#             'date_desp':datetime.now(),
#             'user_desp_id':self.env.user.id,
#         })
        
#     @api.onchange('move_line_ids_without_package.qty_received', 'move_ids_without_package.qty_received')
#     def onchange_qty_received(self):
        
#         # print(op2222)
        
#         raise UserError('test 111111111111111=================> %s' %(self))
        
        
    
    
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super(stockPicking, self).create(vals_list)
        
        if res.picking_type_id.sequence_code == 'SALIDA' and not res.cost_id:
            raise UserError('Para operaciones de tipo despacho es necesario una requisicion.')
        return res
    
    def write(self, vals):
        res = super(stockPicking, self).write(vals)
        
        if vals.get('move_line_ids_without_package'):
            self.write({
                'date_desp':datetime.now(),
                'user_desp_id':self.env.user.id,
            })

        # raise UserError('test 111111111111111=================> %s' %(vals))
        if self.picking_type_id.sequence_code == 'SALIDA' and not self.cost_id:
            raise UserError('Para operaciones de tipo despacho es necesario una requisicion.')
        return res
    
    def action_confirm_quantity_inventary(self):
        # pass
        for line in self.move_ids_without_package:
            line.write({
                'qty_received':line.quantity_done
            })
            
        for line in self.move_line_ids_without_package:
            line.write({
                'qty_received':line.qty_done
            })
            
        self.write({
            'date_desp':datetime.now(),
            'user_desp_id':self.env.user.id,
        })