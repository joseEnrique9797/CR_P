from odoo.tools.translate import _
from odoo import api, fields, models, _
from odoo.exceptions import UserError,Warning,ValidationError
import json

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    name = fields.Char('Solicitud de presupuesto', copy =False)
    type = fields.Selection([ ('default', 'por definir') ,('croc', 'CROC'),('rtop', 'RTOP'),('crop', 'CROP'),],'Tipo', default='default',required=True, copy = False)
    is_import = fields.Boolean(string='Importación')    
    note_description = fields.Text(string='Descripción')
    import_states_id = fields.Many2one('import.states', string='Estado de Importación')
    
    contact = fields.Many2one('res.partner', string='Contact')
    
    quote_number = fields.Char('QUOTE NUMBER')
    ref_project = fields.Char('REF. PROJECT')
    
    notify_to = fields.Many2many('res.partner', string='Notify To')
    ship_to = fields.Many2one('res.partner', string='Ship To [RTOP]')
    bill_to = fields.Many2one('res.partner', string='Bill To [RTOP]')
    rtop_partner_id = fields.Many2one('res.partner', string='RTOP Company',compute='get_rtop_partner')
    
    ship_to_crop_id = fields.Many2one('res.partner', string='Ship To [CROP]')
    bill_to_crop_id = fields.Many2one('res.partner', string='Bill To [CROP]')
    crop_partner_id = fields.Many2one('res.partner', string='CROP Company',compute='get_crop_partner')
    
    po_description = fields.Html('')

    @api.onchange('type')
    def onchange_type(self):
        purchase_seq = self.env['ir.sequence']
        name = purchase_seq.next_by_code('purchase.order.%s' % self.type)
        self.write({
            'name':name
        })
    
    @api.model
    def default_get(self,fields):
        res = super(PurchaseOrder,self).default_get(fields)
        rtop_partner_id = self.env['res.partner'].search([('for_rtop_report','=',True)],limit=1) or False
        crop_partner_id = self.env['res.partner'].search([('for_cro_report','=',True)],limit=1) or False
        html_builder = """ 
                        <table class="table table-bordered">
                            <tbody>
                                <tr>
                                    <td style="width:115px;">
                                        <strong><font style="font-size: 14px;">Instrucciones:</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <strong><font style="font-size: 14px;">Consignatario:</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <strong><font style="font-size: 14px;">Enviar a:</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <strong><font style="font-size: 14px;">Referencia:</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <strong><font style="font-size: 14px;">Contactar a:</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <strong><font style="font-size: 14px;">Dirección de</font></strong>
                                    </td>
                                    <td></td>
                                </tr>
                                <tr>
                                    <td>
                                        <font style="font-size: 14px;">Observaciones:</font>
                                    </td>
                                    <td></td>
                                </tr>
                            </tbody>
                        </table>
                        <table class="table table-bordered">
                            <tbody>
                                <tr>
                                    <td rowspan="2">Departamento: </td>
                                    <td>Solicita:</td>
                                </tr>
                                <tr>
                                    <td>Autoriza:</td>
                                </tr>
                                <tr>
                                    <td colspan="2">
                                    <p style="text-align:center;font-size:14px;"><strong>FAVOR EMITIR LA FACTURA A NOMBRE DE REGULACIÓN Y MANEJO DE</strong></p>
                                    <p style="text-align:center;font-size:14px;"><strong>FLUIDOS R&amp;M DE COSTA RICA S.A.</strong></p>
                                    <p style="text-align:justify;font-size:14px;">Para su pago debe presentar: Original de Factura acompañado del original de esta Orden de Compra, además del original de recibo de mercancías por parte del cliente.</p>
                                    </td>
                                </tr>
                                </tbody>
                        </table>
                        
        """
        res.update({
            'rtop_partner_id': rtop_partner_id,
            'crop_partner_id': crop_partner_id,
            'po_description': html_builder,
        })
        return res
    
    def get_clean_html(self):
        html_builder = self.po_description.replace("table table-bordered", "table table-borderless",1)
        html_builder = html_builder.replace("table table-bordered","table table-borderless border border-4 border-dark",1)
        html_builder = html_builder.replace("""<td colspan="2">""", """<td colspan="2" style="border-top:1px solid black;">""",1)
        return html_builder
    
    @api.depends('rtop_partner_id')
    def get_rtop_partner(self):
        for rec in self:
            rtop_partner_id = self.env['res.partner'].search([('for_rtop_report','=',True)],limit=1)
            rec.rtop_partner_id = rtop_partner_id
            
    @api.depends('crop_partner_id')
    def get_crop_partner(self):
        for rec in self:
            crop_partner_id = self.env['res.partner'].search([('for_cro_report','=',True)],limit=1)
            rec.crop_partner_id = crop_partner_id
            
    
    @api.onchange('rtop_partner_id','crop_partner_id','bill_to','ship_to','notify_to')
    def onchange_rtop_partner_id(self):
        res = {}
        if self.rtop_partner_id or self.crop_partner_id:
            res = {
                    'domain': {
                        'bill_to': [('id','in', (self.rtop_partner_id.child_ids.filtered(lambda x: x.type == 'invoice')).ids )],
                        'ship_to': [('id','in', (self.rtop_partner_id.child_ids.filtered(lambda x: x.type == 'delivery')).ids )],
                        'bill_to_crop_id': [('id','in', (self.crop_partner_id.child_ids.filtered(lambda x: x.type == 'invoice')).ids )],
                        'ship_to_crop_id': [('id','in', (self.crop_partner_id.child_ids.filtered(lambda x: x.type == 'delivery')).ids )],
                    }
                }
        return res
    
    @api.model
    def create(self, vals):
        vals.update({
            'name': 'Por definir tipo',
        })
        
        res = super(PurchaseOrder, self).create(vals)
        # purchase_seq = self.env['ir.sequence']
        # res.name = purchase_seq.next_by_code('purchase.order.%s' % res.type)
        # res.name = '
        if not res.name: 
            res.name = 'Por definir tipo'
        return res
    
    # Update the context to set the template based on the report type
    def action_rfq_send(self):
        res = super(PurchaseOrder, self).action_rfq_send()
        ctx = dict(self.env.context or {})
        ir_model_data = self.env['ir.model.data']
        template_id = False
        if self.type=='rtop':
            template_id = ir_model_data.get_object_reference('cr_sale_rymca', 'email_template_rtop')[1]
        if self.type=='crop':
            template_id = ir_model_data.get_object_reference('cr_sale_rymca', 'email_template_crop')[1]
        if self.type=='croc':
            template_id = ir_model_data.get_object_reference('cr_sale_rymca', 'email_template_croc')[1]
        
        
        # raise UserError("Only admins can upload SVG files. %s" %template_id)
        ctx.update({'default_use_template':False,'default_template_id':template_id})
        res.update({'context':ctx})
        return res