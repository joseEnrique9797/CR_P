from odoo import _, api, fields, models, tools

from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)
class createDespachos(models.Model):
    _name = 'create.despachos'
    

    cost_id = fields.Many2one('job.cost.sheet', string='Requisicion', required = True)
    cost_ids = fields.Many2many('job.cost.sheet', string='Requisiciones')
    product_desp = fields.Integer('Cantidad a despachar')
    product_id = fields.Many2one('product.product', string='Producto')
    product_desp_max = fields.Integer('Cantidad a despachar')
    
    
    def action_confirm(self):
        product_desp_max = 0
        for rec in self.cost_id.material_job_cost_line_ids:
            if rec.product_id.id == self.product_id.id :
                product_desp_max += rec.qty_pending
        if self.product_desp > product_desp_max:
            raise UserError('No puede despachar mas de la cantidad consolidada del producto')
        
        stock = self.env['stock.picking.type'].search([
            ('name', '=', 'Despachos')
        ])
        
        location_dest_id = self.env['stock.location'].search([
            ('name', '=', 'Customers')
        ])
        
        uom_uom = self.env['uom.uom'].search([
            ('name', '=', 'Unidad')
        ], limit = 1)  
        
        if not uom_uom:
            uom_uom = self.env['uom.uom'].search([
                ('name', '=', 'Unidades')
            ], limit = 1) 
        
        if not stock or not location_dest_id:
            raise UserError('Configure una transferencia de tipo despacho o locacion')
        
        
        
        lines = []
        lines.append( (0,0,{
            'name':'Borrador', 
            'product_id':self.product_id.id, 
            'product_uom_qty':self.product_desp,
            'product_uom':uom_uom.id,
            
        }) )
#         raise UserError('Configure una transferencia de tipo despacho %s' %stock)
        vals = {
#             'name': 'Borrador',
            'cost_id': self.cost_id.id,
            'picking_type_id': stock.id,
            'location_id': stock.default_location_src_id.id,
            'location_dest_id': location_dest_id.id,
            'analytic_account_id': self.cost_id.analytic_account_id.id,
            'move_ids_without_package': lines,
        }
        
        obj = self.env['stock.picking'].create(vals)
        return {
            'name': 'Despacho',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', '=', obj.id)],
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    
class jobCostSheetConsolidation(models.Model):
    _name = 'job.cost.sheet.consolidation'
    
    cost_sheet_ids = fields.Many2many('job.cost.sheet', string='Requisiciones', compute = 'get_cost_and_lines')
    block_dates = fields.Boolean('')
    create_by_id = fields.Many2one('res.users', string='Creado por')
    cost_count = fields.Integer('Despachos', compute = 'get_cost_count')
    name = fields.Char('Numero')
    create_date = fields.Datetime('Fecha Requerido', copy=False)
    date_init = fields.Date('Desde', required=True)
    date_end = fields.Date('Hasta', required=True)
    state = fields.Selection([
        ('open', 'Abierto'),
        ('close', 'Cerrado')
    ], string='Estado', default = 'open')
#     
    consolidation_line_ids = fields.One2many('job.cost.sheet.consolidation.line', 'consolidation_id', string='Lineas')
    
    def get_cost_and_lines(self):
        for rec in self:
            rec.cost_sheet_ids = False
            rec.consolidation_line_ids = False
            
            cost = rec.env['job.cost.sheet'].search([
                ('stage', 'in', ['confirm', 'approve']),
                ('consolidation_id', '=',self.id ),
            ])

            consolidate = rec.env['job.cost.sheet.consolidation']
            
            product_ids = []
            lines = []
            for line in cost.material_job_cost_line_ids.filtered(lambda m: m.qty_pending > 0 ):
                
                
                # if line.id != 11087:
                #     raise UserError('=====================>. %s'%(line.qty_pending))
                # qty_wait = 0 
                # for co in cost:
                #     for line_cost in co.material_job_cost_line_ids:
                #         if line.product_id.id == line_cost.product_id.id:
                #             qty_wait +=  line_cost.qty_pending
                
                # and qty_wait > 0
                
                if line.product_id.id not in product_ids :
                    product_ids.append(line.product_id.id)
                    lines.append((0,0,{
                        'product_id': line.product_id.id,
                        'consolidation_id': rec.id,
                        'consolidation_int': rec.id,
                    }))
            # Aceite corte/rosca rigid (galón)
            rec.write({
                'cost_sheet_ids': [(6,0, cost.ids)],
                'consolidation_line_ids': lines,
            })
    
    def get_cost_count(self):
        for rec in self:
            rec.cost_count = len(rec.cost_sheet_ids)

    @api.model
    def create(self, values):
        res = super(jobCostSheetConsolidation, self).create(values)
        
        if not res.cost_sheet_ids:
            cost = res.env['job.cost.sheet'].search([
                ('stage', 'in', ['confirm', 'approve']),
                ('create_date_', '>=',values['date_init'] ),
                ('create_date_', '<=',values['date_end'] ),
            ])

            if not cost:
                res.date_init = False
                res.date_end = False
                raise UserError('No hay hojas de costos para las fechas establecidas.')
            
            for c in cost:
                c.consolidation_id = res.id
            
            res.block_dates = True
            
        
        res.name = datetime.now().strftime("%Y") +'/'+ datetime.now().strftime("%m") +self.env['ir.sequence'].next_by_code('sheet.consolidation')
        
        return res
    
    
    def cost_list_get(self):
        return {
            'name': 'Requisiciones',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'job.cost.sheet',
            'domain': [('id', 'in', self.cost_sheet_ids.ids)],
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        
    
    #@api.model
    def default_get(self, field_list):
        res = super(jobCostSheetConsolidation, self).default_get(field_list)
        
#         raise UserError('data=================> %s' %( datetime.now().strftime("%m") ))
        
        res.update({
            'create_date': datetime.now(),
            'create_by_id': self.env.user.id,
        })
        return res
        
class jobCostSheetConsolidationLine(models.Model):
    _name = 'job.cost.sheet.consolidation.line'
        
    consolidation_id = fields.Many2one('job.cost.sheet.consolidation', string='Consolidacion')
    consolidation_int = fields.Integer(string='')
    description = fields.Char('Descripción del producto')
    product_id = fields.Many2one('product.product', string='Producto')
    description = fields.Text('Descripción del producto', related = 'product_id.description' )
    qty_required = fields.Float('Cantidad solicitada', compute = 'get_values_qty')
    qty_send = fields.Float('Cantidad despachada', compute = 'get_values_qty')
    qty_wait = fields.Float('Cantidad pendiente', compute = 'get_values_qty')
    qty_head = fields.Float('Cantidad a Mano',  related = 'product_id.qty_available')

    # @api.model
    def get_despachos(self):
#         print(op777)

        array = []

        consolidation_id = self.env['job.cost.sheet.consolidation'].browse([self.consolidation_int])
        
        # raise UserError('=====================>. %s'%(consolidation_id))
        for rec in consolidation_id.cost_sheet_ids:
            for line in rec.material_job_cost_line_ids:
                if line.product_id.id == self.product_id.id:
                    if rec.id not in array:
                        array.append(rec.id)
        return {
            'name': 'Despachos',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'create.despachos',
            'context': {'default_cost_ids': array, 'default_product_id': self.product_id.id, 'default_product_desp': 1, 'default_product_desp_max': self.qty_wait},
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    
    # @api.depends('')
    def get_values_qty(self):
        for rec in self:
            rec.qty_required = 0
            rec.qty_send = 0
            rec.qty_wait = 0
#             rec.qty_head = 0
            # _logger.warning('data ===222============== %s',  line_cost.product_id )
            consolidation_id = rec.consolidation_id
            if not consolidation_id:
                consolidation_id = self.env['job.cost.sheet.consolidation'].browse([rec.consolidation_int])
            
            for cost in consolidation_id.cost_sheet_ids:
                # raise UserError('data=================> %s' %( cost.material_job_cost_line_ids ))
                for line_cost in cost.material_job_cost_line_ids.filtered(lambda m: m.product_id.id == rec.product_id.id):
                    
                    # if rec.product_id.id == line_cost.product_id.id:
                    rec.qty_required +=  line_cost.quantity
                    rec.qty_send +=  line_cost.qty_desp
                    rec.qty_wait +=  line_cost.qty_pending
            
            
class jobCostSheet(models.Model):
    _inherit = 'job.cost.sheet'
    
    
    impreso = fields.Boolean('Impreso')
    consolidation_id = fields.Many2one('job.cost.sheet.consolidation', string='Consolidacion')
    
    desp_exp_date = fields.Datetime('fecha llamado Fecha Expedito')
    desp_exp = fields.Boolean('Despacho expedito')
    create_date_ = fields.Datetime('Fecha Requerido', copy=False)
    date_confirm = fields.Datetime('Fecha de confirmación', copy=False)
    date_requested  = fields.Datetime('fecha de la solicitud', copy=False)
    date_ending = fields.Datetime('Fecha de finalización', copy=False)
    date_cancel = fields.Datetime('Fecha de cancelación', copy=False)
    user_cancel_id = fields.Many2one('res.users', string='Usuario cancelacion')
    reason = fields.Char('Motivo de cancelacion')
    compute_all_product = fields.Char('', store = True, compute = 'get_compute_all_product')
#   field_name = fields.Date('field_name')
    inventory_count = fields.Integer('Despachos', compute = 'get_inventory_count')
    stage = fields.Selection(selection_add=[("cancel", "Cancelado"), ("desp", "Despachado"), ("consolidate", "Consolidado") ]    )
    
    
    pending = fields.Boolean('')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta analitica', required = True)
    
    
    def action_confirm_desp(self):
        
        stock = self.env['stock.picking.type'].search([
            ('name', '=', 'Despachos')
        ])
        
        location_dest_id = self.env['stock.location'].search([
            ('name', '=', 'Customers')
        ])
        
        uom_uom = self.env['uom.uom'].search([
            ('name', '=', 'Unidad')
        ], limit = 1)  
        
        if not uom_uom:
            uom_uom = self.env['uom.uom'].search([
                ('name', '=', 'Unidades')
            ], limit = 1)  
        
        if not stock or not location_dest_id:
            raise UserError('Configure una transferencia de tipo despacho o locacion')
        
        
        
        lines = []
        
        
        for l in self.material_job_cost_line_ids:
            
            if l.qty_pending > 0:
                lines.append( (0,0,{
                    'name':'Borrador', 
                    'product_id':l.product_id.id, 
                    'product_uom_qty':l.qty_pending,
                    'product_uom':uom_uom.id,
    
                }) )

        if not lines:
            raise UserError('Esta requisicion ya no tiene cantidades que despachar.')
        
        
        vals = {
#             'name': 'Borrador',
            'cost_id': self.id,
            'picking_type_id': stock.id,
            'location_id': stock.default_location_src_id.id,
            'location_dest_id': location_dest_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'move_ids_without_package': lines,
        }
        
        stock_create = self.env['stock.picking'].create(vals)
        
        
        return {
            'name': 'Despacho',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('id', '=', stock_create.id)],
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    
    
    def action_approve(self):
        result = super(jobCostSheet, self).action_approve() 
        self.action_done()
        return result
    
    
    #@api.model
    def default_get(self, field_list):
        res = super(jobCostSheet, self).default_get(field_list)
        
        res.update({
            'create_by_id': self.env.user.id,
#             'name': self.env.user.id,
            'date_requested': datetime.now(),
        })
        return res
    
    def action_confirm_close(self):
        self.stage = 'desp'
    
    def get_inventory_count(self):
        for rec in self:
            rec.inventory_count = len(rec.env['stock.picking'].search([
                ('cost_id', '=', rec.id),
#                 ('state', '=', 'done'),
            ]))
            
#             self.get_pending()
    
    def inventory_get(self):
        return {
            'name': 'Despachos',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('cost_id', '=', self.id)],
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    
    @api.depends('material_job_cost_line_ids')
    def get_compute_all_product(self):
        for rec in self:
            rec.compute_all_product = ''
            for line in rec.material_job_cost_line_ids:
                rec.compute_all_product += line.product_id.name + ' '  if line.product_id else ' '
    
    def action_confirm(self):
        self.close_date = datetime.now()
        self.date_confirm = datetime.now()
        result = super(jobCostSheet, self).action_confirm()
        return result
    
    
    
#     @api.onchange('inventory_count')
#     @api.depends('inventory_count')
#     def get_pending(self):
#         for rec in self:
#             rec.pending = False
#             if rec.material_job_cost_line_ids:
#                 for line in rec.material_job_cost_line_ids:
#                     if line.qty_pending > 0:
#                         rec.pending = True

#                 if rec.pending == False:
#     #                 raise UserError('pending=================> %s' %(rec.stage))
#                     rec.write({
#                         'stage': 'desp'
#                     }) 
#             else:
#                 rec.pending = True
    
    
#     def write(self, values):

#         res = super(jobCostSheet, self).write(values)
        
#         if self.create_date_ :
#             result_days =  (datetime.now() - self.create_date_  ).days
# #             raise UserError('data=================> %s' %(result_days))
#             if result_days > -3:
#                 raise UserError('La fecha requerido tiene que ser minimo 3 dias despues de hoy.')
        
#         return res

    
    
    
    @api.model
    def create(self, values):
#         raise UserError('data======2222===========> %s' %( values))
        res = super(jobCostSheet, self).create(values)
        if res.create_date_ :
            result_days =  (datetime.now() - res.create_date_  ).days
            if result_days > -3:
                raise UserError('La fecha requerido tiene que ser minimo 3 dias despues de hoy.')
        
        return res
        
    def action_confirm_cancel(self):
        return {
            'name': 'Cancelacion',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'job.cost.sheet.wizard.cancel',
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        
        
class jobCostLine(models.Model):
    _inherit = 'job.cost.line'
    
    qty_desp = fields.Float('Cantidad despachada', compute= 'get_qty_desp_all')
    qty_pending = fields.Float('Cantidad pendiente', compute= 'get_qty_desp_all')
    
    def get_qty_desp_all(self):
        for rec in self:
            rec.qty_desp = 0
            rec.qty_pending = 0
            inventories = rec.env['stock.picking'].search([
                ('cost_id', '=', rec.material_job_cost_sheet_id.id)
            ])
#             raise UserError('data=================> %s' %(rec.material_job_cost_sheet_id))
            for inv in inventories:
                for move in inv.move_line_ids_without_package:
#                     print(op4444)
                    if move.product_id.id == rec.product_id.id:
#                         print(op5555)
                        rec.qty_desp += move.qty_done
    
            rec.qty_pending  = rec.quantity - rec.qty_desp
            
#             pass