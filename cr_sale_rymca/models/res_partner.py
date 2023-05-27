from odoo.tools.translate import _
from odoo import api, fields, models, _
from odoo.exceptions import UserError,Warning,ValidationError

class resPartner(models.Model):
    _inherit = 'res.partner'
    
    for_rtop_report = fields.Boolean('Reporte RTOP')
    for_cro_report = fields.Boolean('Reporte CROP')
    
    fax = fields.Char('Fax')
    po_box = fields.Char('P.O. Box')