from odoo.tools.translate import _
from odoo import api, fields, models, _
from odoo.exceptions import UserError,Warning,ValidationError

class ImportStates(models.Model):
    _name = 'import.states'
    
    name = fields.Char(string='Nombre', required=True, store=True)
    active_state = fields.Boolean(string='Activo', store=True)