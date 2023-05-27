from odoo.tools.translate import _
from odoo import api, fields, models, _
from odoo.exceptions import UserError,Warning,ValidationError

class resCompany(models.Model):
    _inherit = 'res.company'
    
    image_rtop = fields.Binary('Imagen reporte')
    
    street_rtop = fields.Char('Direccion 1')
    street_rtop2 = fields.Char('Direccion 2')
    city_rtop = fields.Char('Ciudad')
    mobil_rtop = fields.Char('Telefono')
    
    