from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class FinancialStatementWizard(models.TransientModel):
    _name = 'financial.statement.wizard'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    all_invoice = fields.Boolean(string='Todas las facturas')
    
    employee_ids = fields.Many2many(comodel_name='hr.employee', string='Notificación de pago', required = True)
    
    template_id = fields.Many2one(comodel_name='mail.template', string='Plantilla de correo')
    
    subject_email  = fields.Char(string='Asunto')
    body_email = fields.Text(string='Cuerpo')
    
    send_mail = fields.Boolean(string='Enviar mail')
    
    def action_get_report(self):
        
        lines_account = self.env['account.move'].search([
            ('partner_id','=', self.env.context.get('partner_id', False) ),
        ])
        if not lines_account:
            raise ValidationError('No hay facturas disponibles para este cliente.')
        
        data = {'start_date': self.start_date, 'end_date': self.end_date, 'all_invoice': self.all_invoice, 'employee_ids': self.employee_ids.ids, 'date':datetime.now().date()}
        data['partner_id'] = self.env.context.get('partner_id', False)
        
        # data['model'] = 'retention.report.wizard'
        # data['form'] = self.read()[0]
        # for field in data['form'].keys():
        #     if isinstance(data['form'][field], tuple):
        #         data['form'][field] = data['form'][field][0]
        return self.env.ref('cr_financial_statement_report.action_financial_statement_report').report_action(self, data=data)
    
    def action_get_report_send_mail(self):
        partner = self.env['res.partner'].browse(self.env.context.get('partner_id', False))
        mail = ''
        
        for rec in self.employee_ids:
            if rec.work_email:
                mail += rec.work_email +','
        
        partner.write({
            'send_email':mail,
            'subject_email':self.subject_email,
            'body_email':self.body_email
        })
        
        self.template_id.send_mail(partner.id)
        
        
    def action_get_report_pdf(self):
        partner = self.env['res.partner'].browse(self.env.context.get('partner_id', False))
        
        if self.start_date and self.end_date:
            partner.start_date =  self.start_date
            partner.end_date = self.end_date
        else :
            partner.start_date =  False
            partner.end_date = False
        
        return self.env.ref('cr_financial_statement_report.report_state_client').report_action(partner.id)
    

    @api.model
    def default_get(self, default_fields):
        rec = super(FinancialStatementWizard, self).default_get(default_fields)
        mail_template = self.env.ref ('cr_financial_statement_report.email_template_report_state')
        rec['template_id'] = mail_template.id
        rec['subject_email'] = 'Estado de Situación Financiera'
        rec['body_email'] = 'Saludos, se adjunta su estado financiero.'
        
        return rec