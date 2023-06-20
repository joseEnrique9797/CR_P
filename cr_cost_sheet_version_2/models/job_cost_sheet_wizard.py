from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class jobCostSheetWizard(models.TransientModel):
    _name = "job.cost.sheet.wizard.cancel"
    
    reason = fields.Char('Motivo de cancelacion', required = True)
    
    def action_confirm(self):
        obj = self.env['job.cost.sheet'].browse(self._context.get('active_id'))
        
        obj.date_cancel = datetime.now()
        obj.stage = 'cancel'
        obj.reason = self.reason
        obj.user_cancel_id = self.env.user.id
   


class consolidateCost(models.TransientModel):
    _name = "consolidate.cost"
    
    date_init = fields.Date('Desde', required = True)
    date_end = fields.Date('Hasta', required = True)
    
    def confirm_consolidate(self):
        cost = self.env['job.cost.sheet'].search([
            ('stage', 'in', ['confirm', 'approve']),
            ('create_date_', '>=',self.date_init ),
            ('create_date_', '<=',self.date_end ),
        ])
        
        if not cost:
            raise UserError('No hay hojas de costos para las fechas establecidas.')
        
        consolidate = self.env['job.cost.sheet.consolidation']
        
        product_ids = []
        lines = []
        for rec in cost.material_job_cost_line_ids:
            if rec.product_id.id not in product_ids:
                product_ids.append(rec.product_id.id)
                lines.append((0,0,{
                    'product_id': rec.product_id.id
                }))
        
        
        obj = consolidate.create({
            'name': datetime.now().strftime("%Y") +'/'+ datetime.now().strftime("%m") +self.env['ir.sequence'].next_by_code('sheet.consolidation'),
            'cost_sheet_ids': [(6,0, cost.ids)],
            'consolidation_line_ids': lines,
            'date_init': self.date_init,
            'date_end': self.date_end,
            'state': 'open',
        })
        
        
        
        return {
            'name': 'Consolidación',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'job.cost.sheet.consolidation',
            'domain': [('id', '=', obj.id)],
#             'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


        
        