# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from datetime import datetime
# from datetime import timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    limit_credit_colones = fields.Float(string='Límite de crédito colones')
    
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    
    send_email = fields.Char(string='Enviar a')
    subject_email  = fields.Char(string='Asunto')
    body_email = fields.Char(string='Cuerpo')
    
    def get_datetime_now(self):
        return datetime.now().date()
        
        
    @api.model
    def action_financial_statement(self,record):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Estado de Situación Financiera',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'financial.statement.wizard',
            'views': [(self.env.ref("cr_financial_statement_report.financial_statement_wizard_view").id, 'form')],
            'context': "{'partner_id':%s}" % record.id,
            'target': 'new',
        }

    # def date_end_date()
    #     return 
    
    def get_dateresultdays(self, invoice_payment_term_id, invoice_date_due):
        if invoice_date_due:
            
#             days_due = invoice_payment_term_id.line_ids[0].days
#             date_ve = invoice_date + timedelta(days=int(days_due))

#             dateresult = date_ve - invoice_date
#             dateresultdays = dateresult.days

            dateresult = datetime.now().date() - invoice_date_due
            dateresultdays = dateresult.days * -1
            
            # if dateresultdays < 0:
            #     dateresultdays = dateresultdays*-1
            # else:
            #     dateresultdays = 0
            
            
            return dateresultdays
        else :
            return 0

    
    def get_restante(self, all):
        lines_account = self.get_accounts_partner()
        restante = 0
        total_colones = 0
        total_dolares = 0
        
        total_importe_colones = 0
        total_importe_dolares = 0
        
        total_devoluciones_colones = 0
        total_devoluciones_dolares = 0
        
        tarifa_currency = self.property_product_pricelist.currency_id if self.property_product_pricelist else False
        tarifa_currency_symbol = tarifa_currency.name if tarifa_currency else ''
        
        for res in lines_account:
            dev  =  res.amount_total - res.amount_residual 
            
            if res.currency_id.name == 'USD':
                total_dolares += res.amount_residual
                total_importe_dolares += res.amount_total 
                total_devoluciones_dolares += dev
                
            if res.currency_id.name == 'CRC':
                total_colones += res.amount_residual
                total_importe_colones += res.amount_total
                total_devoluciones_colones += dev
                
        total_mont_convert = total_colones + (total_dolares * tarifa_currency.rate) 
        restante = all - total_mont_convert
        return restante
    
    
    
    def get_total_mont_convert(self):
        lines_account = self.get_accounts_partner()
        restante = 0
        total_colones = 0
        total_dolares = 0
        
        total_importe_colones = 0
        total_importe_dolares = 0
        
        total_devoluciones_colones = 0
        total_devoluciones_dolares = 0
        
        tarifa_currency = self.property_product_pricelist.currency_id if self.property_product_pricelist else False
        tarifa_currency_symbol = tarifa_currency.name if tarifa_currency else ''
        
        for res in lines_account:
            dev  =  res.amount_total - res.amount_residual 
            
            if res.currency_id.name == 'USD':
                total_dolares += res.amount_residual
                total_importe_dolares += res.amount_total 
                total_devoluciones_dolares += dev
                
            if res.currency_id.name == 'CRC':
                total_colones += res.amount_residual
                total_importe_colones += res.amount_total
                total_devoluciones_colones += dev
                
        total_mont_convert = total_colones + (total_dolares * tarifa_currency.rate) 
        return total_mont_convert
        
    
    def get_limite_tarifa_credito(self):
        
        tarifa_currency = self.property_product_pricelist.currency_id if self.property_product_pricelist else False
        tarifa_currency_symbol = tarifa_currency.name if tarifa_currency else ''
        
        limite_tarifa_credito = 0
        if tarifa_currency_symbol == 'CRC':
            limite_tarifa_credito = self.limit_credit_colones
        
        if tarifa_currency_symbol == 'USD':
            limite_tarifa_credito = self.limit_credit
        
        return limite_tarifa_credito

    def date_end_date(self, line):

        if line.invoice_payment_term_id and line.invoice_payment_term_id.line_ids:
            return line.invoice_date_due + timedelta(days=line.invoice_payment_term_id.line_ids[0].days)
        else :
            return line.invoice_date_due

    
    def get_accounts_partner(self):
        if self.start_date and self.end_date:
            lines_account = self.env['account.move'].search([
                ('partner_id','=', self.id ),
                ('invoice_date','>=', self.start_date ),
                ('invoice_date','<=', self.end_date ),
                ('move_type','in', ['out_invoice'] ),
                ('state','in', ['posted'] ),
            ])

            lines_filtered = []
            for l in lines_account:
                if l.amount_total  - l.amount_residual > 0:
                    lines_filtered.append(l.id)

            
            lines_account = self.env['account.move'].browse(lines_filtered)

            
            self.start_date = False
            self.end_date = False

            
            return lines_account
        else:
            lines_account = self.env['account.move'].search([
                ('partner_id','=', self.id ),
                ('move_type','in', ['out_invoice'] ),
                ('state','in', ['posted'] ),
            ])
            lines_filtered = []
            for l in lines_account:
                if l.amount_total  - l.amount_residual > 0:
                    lines_filtered.append(l.id)

            
            # lines_account = self.env['account.move'].browse(lines_filtered)
            
            return lines_account

        
            
            
    