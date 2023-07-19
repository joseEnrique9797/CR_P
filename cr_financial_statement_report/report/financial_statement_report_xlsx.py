# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import timedelta
import io
import base64

from bs4 import BeautifulSoup

class RetentionReportXls(models.AbstractModel):
    _name = 'report.cr_financial_statement_report.financial_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        
        sheet = workbook.add_worksheet(_('Financial Statement Report'))
        format1 = workbook.add_format(
            {'font_size': 14, 'bottom': False, 'right': False, 'left': False, 'top': False, 'align': 'center',
                'bold': True})
        format4 = workbook.add_format({'align':'center', 'left':True, 'right':True, 'bottom': True, 'top': True, 'font_size': 10,'num_format': '#,##0.00', 'bold': True, 'bg_color':'#dbeb34'})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'font_color':'#ffffff','bg_color':'#000000'})
        format22 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': False, 'text_wrap': True})
        format24 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': False, 'text_wrap': True, 'num_format': '#,##0.00'})
        
        format30 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': False, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format31 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': False, 'top': False, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format32 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': True, 'top': False, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format33 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        
        format34 = workbook.add_format({'font_size': 10, 'valign':'middle', 'align': 'center', 'right': False, 'left': True,'bottom': True, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        
        format35= workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'valign':'middle', 'align': 'right', 'right': False, 'left': False,'bottom': True, 'top': False, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format36= workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'valign':'middle', 'align': 'right', 'right': True, 'left': False,'bottom': False, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format37= workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'valign':'middle', 'align': 'right', 'right': False, 'left': False,'bottom': False, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format38= workbook.add_format({'font_size': 10, 'valign':'middle', 'align': 'center', 'right': False, 'left': False,'bottom': True, 'top': True, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        format39= workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'valign':'middle', 'align': 'right', 'right': True, 'left': False,'bottom': True, 'top': False, 'bold': True, 'text_wrap': True,'bg_color':'#D9E1F2'})
        
        
        
        format40 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True,'bottom': False, 'top': True, 'bold': True, 'text_wrap': True})
        format41 = workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'align': 'right', 'right': True, 'left': True,'bottom': False, 'top': False, 'bold': True, 'text_wrap': True})
        format42 = workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'align': 'right', 'right': True, 'left': True,'bottom': True, 'top': False, 'bold': True, 'text_wrap': True})
        format43 = workbook.add_format({'num_format': '#,##0.00','font_size': 10, 'align': 'right', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'text_wrap': True})
        
        format50 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True, 'text_wrap': False,'underline':1})
        format51 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': True, 'text_wrap': True})
        format52 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'left': False,'bottom': False, 'top': False, 'bold': False, 'text_wrap': False})
        
        
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 18)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 18)
        sheet.set_column(4, 4, 18)
        sheet.set_column(5, 5, 28)
        sheet.set_column(6, 6, 17)
        sheet.set_column(7, 7, 30)
        sheet.set_column(8, 8, 15)
        sheet.set_column(9, 9, 15)
        sheet.set_column(10, 10, 15)
        sheet.set_column(11, 11, 15)
        sheet.set_column(12, 12, 15)
        sheet.set_column(13, 13, 15)
        sheet.set_column(14, 14, 15)
        sheet.set_column(15, 15, 15)
        sheet.set_column(16, 16, 15)
        
        
        # Variables
        partner_id = self.env['res.partner'].search([('id','=',data.get('partner_id'))])
        result = ['1'] # Here we make a method to gather the info to fill the report
        company_logo = io.BytesIO(base64.b64decode(self.env.company.favicon))
        
        # Header
        sheet.insert_image(0,0,"company.png",{'image_data': company_logo,'x_scale': .25, 'y_scale': .25})
        sheet.merge_range('C2:J2',self.env.company.name,format1)
        sheet.merge_range('C3:J3','Estado de Cuenta - Cuentas por Cobrar',format1)
        sheet.write(4,2,'Fecha de Corte',format51)
        sheet.write(4,3, str(data['date']) ,format52)
        
        
        
        
        tarifa_currency = partner_id.property_product_pricelist.currency_id if partner_id.property_product_pricelist else False
        tarifa_currency_symbol = tarifa_currency.name if tarifa_currency else ''
        
        limite_tarifa_credito = 0
        if tarifa_currency_symbol == 'CRC':
            limite_tarifa_credito = partner_id.limit_credit_colones
        
        if tarifa_currency_symbol == 'USD':
            limite_tarifa_credito = partner_id.limit_credit
        
        
        # First
        sheet.write(7,0,'CÓDIGO',format30)
        sheet.merge_range('B8:H8',partner_id.code,format40)
        sheet.write(7,8,'PLAZO CRÉDITO',format30)
        sheet.write(7,9, partner_id.property_payment_term_id.name,format40)
        
        sheet.write(8,0,'CLIENTE',format31)
        sheet.merge_range('B9:H9',partner_id.name,format41)
        sheet.write(8,8,'LIMITE CRÉDITO' + ' (' +tarifa_currency.name + ')',format31)
        sheet.write(8,9, limite_tarifa_credito ,format41)
        
        sheet.write(9,0,'CONTRIBUYENTE',format31)
        sheet.merge_range('B10:H10', partner_id.vat,format41)
        sheet.write(9,8,'TOTAL CRÉDITO',format31)
        
        
        sheet.write(10,0,'DIRECCIÓN',format31)
        sheet.merge_range('B11:H11',partner_id.contact_address_complete,format41)
        sheet.write(10,8,'DISPONIBLE',format32)
        
        
        sheet.write(11,0,'VENDEDOR',format32)
        sheet.merge_range('B12:H12',partner_id.user_id.name if partner_id.user_id else '',format42)
        # sheet.write(11,8,'SOBREGIRO',format32)
        # sheet.write(11,9,'0',format42)
        
        # Second
        sheet.write(13,0,'FECHA EMISIÓN',format33)
        sheet.write(13,1,'DÍAS CRÉDITO',format33)
        sheet.write(13,2,'FECHA VENCIMIENTO',format33)
        sheet.write(13,3,'REFERENCIA',format33)
        sheet.write(13,4,'MONEDA ORIGEN',format33)
        sheet.write(13,5,'IMPORTE',format33)
        sheet.write(13,6,'ABONOS/DEVOLUCIONES',format33)
        sheet.write(13,7,'SALDO ACTUAL',format33)
        sheet.write(13,8,'ESTADO',format33)
        sheet.write(13,9,'DÍAS DE VENCIMIENTO',format33)
        
        row = 14
        
        
        # raise ValidationError('esta es la data=========>%s' %data)
        
        if data['all_invoice']:
            lines_account = self.env['account.move'].search([
                ('partner_id','=', partner_id.id ),
                ('state','=', 'posted'),
                ('move_type','in', ['out_invoice'] ),
                ('payment_state','in', ['in_payment', 'partial', 'not_paid'] ),
            ])

            lines_filtered = []
            for l in lines_account:
                if l.amount_total  - l.amount_residual > 0:
                    lines_filtered.append(l.id)
            
            lines_account = self.env['account.move'].browse(lines_account.ids)
        
        else:
            lines_account = self.env['account.move'].search([
                ('partner_id','=', partner_id.id ),
                ('state','=', 'posted'),
                ('payment_state','in', ['in_payment', 'partial', 'not_paid'] ),
                ('move_type','in', ['out_invoice'] ),
                ('invoice_date','>=', data['start_date'] ),
                ('invoice_date','<=', data['end_date'] ),
            ])

            lines_filtered = []
            for l in lines_account:
                if l.amount_total  - l.amount_residual > 0:
                    lines_filtered.append(l.id)
            
            lines_account = self.env['account.move'].browse(lines_account.ids)
        
        total_colones = 0
        total_dolares = 0
        
        total_importe_colones = 0
        total_importe_dolares = 0
        
        total_devoluciones_colones = 0
        total_devoluciones_dolares = 0
        for res in lines_account:
            sheet.write(row,0,str(res.invoice_date),format43)
            if res.invoice_payment_term_id and res.invoice_payment_term_id.line_ids and res.invoice_payment_term_id.line_ids[0].days :
                sheet.write(row,1,res.invoice_payment_term_id.line_ids[0].days,format43)
            else :
                sheet.write(row,1,'',format43)


        
            if res and res.invoice_payment_term_id and res.invoice_payment_term_id.line_ids:
                date_ve = res.invoice_date + timedelta(days=res.invoice_payment_term_id.line_ids[0].days)
            else:
                date_ve = res.invoice_date_due
            
            
            # date_ve = res.invoice_date + timedelta(days=int(days_due))
    
            sheet.write(row,2, str(date_ve),format43)
            sheet.write(row,3,res.name,format43)
            sheet.write(row,4,res.currency_id.name,format43)
            sheet.write(row,5,res.amount_total,format43)
            sheet.write(row,6, res.amount_total  - res.amount_residual  ,format43)
            sheet.write(row,7, res.amount_residual  ,format43)
            dev  =  res.amount_total - res.amount_residual 
            
            
            
            dateresultdays = 0
            
            # dateresult = datetime.now().date() - res.invoice_date_due
            # dateresultdays = dateresult.days * -1
            
            if res.invoice_payment_term_id:
            
                invoice_date_due =  res.invoice_date + timedelta(days=res.invoice_payment_term_id.line_ids[0].days)
                dateresult = datetime.now().date() - invoice_date_due
                dateresultdays = dateresult.days 
                # return dateresultdays
            else :
                if res.invoice_date_due:
                    dateresult = datetime.now().date() - res.invoice_date_due
                    dateresultdays = dateresult.days 
                
            
            
            
            
            
            state = 'Sin definir'
            if dateresultdays < 0:
                state = 'No vencida'
            
            elif dateresultdays > 0:
                state = 'Vencida'
           
            	
            # invoice_date_due
            sheet.write(row,8, state ,format43)
            
            sheet.write(row,9,dateresultdays,format43)
            
            if res.currency_id.name == 'USD':
                total_dolares += res.amount_residual
                total_importe_dolares += res.amount_total 
                total_devoluciones_dolares += dev
                
            if res.currency_id.name == 'CRC':
                total_colones += res.amount_residual
                total_importe_colones += res.amount_total
                total_devoluciones_colones += dev
            
            row+=1
        row+=1
        
        # Totals
        sheet.merge_range('A%s:A%s'%(row+1,row+2),'SALDO',format34)
        sheet.merge_range('B%s:D%s'%(row+1,row+2),'',format38)
        
        sheet.write(row,4,'CRC',format37)
        sheet.write(row+1,4,'USD',format35)
        
        sheet.write(row,5, (round(total_importe_colones, 2))   ,format37)
        sheet.write(row+1,5,   (round(total_importe_dolares, 2)),format35)
        
        sheet.write(row,6, (round(total_devoluciones_colones, 2)),format37)
        sheet.write(row+1,6,  (round(total_devoluciones_dolares, 2)),format35)
        
        sheet.write(row,7, (round(total_colones, 2)),format36)
        sheet.write(row+1,7,  (round(total_dolares, 2)),format39)
        
        total_mont_convert = total_colones + (total_dolares * tarifa_currency.rate) 
        sheet.write(9,9,round(total_mont_convert, 2),format41)
        
        restante = limite_tarifa_credito - total_mont_convert
        sheet.write(10,9,round(restante, 2),format42)
        
        # Other Info
        
        row+=3
        sheet.write(row,0,'Información para Depósitos',format50)
        sheet.write(row+2,0,'Razón social',format51)
        sheet.write(row+2,1,self.env.company.name,format52)
        
        partner_comp =  self.env['res.partner'].search([
            ('name', '=', self.env.company.name)
        ], limit = 1)
        
        if partner_comp.l10n_latam_identification_type_id:
            sheet.write(row+3,0,partner_comp.l10n_latam_identification_type_id.name,format51)
        
        
        
        name_comp = ''
        # if partner_comp and partner_comp.l10n_latam_identification_type_id:
        #     name = 
        name_comp += ' ' + partner_comp.vat
        
        sheet.write(row+3,1, name_comp  ,format52)
        
        
        row+=5

        soup = BeautifulSoup(self.env.company.notifi_account_report)
        sheet.write(row,1, soup.get_text()  ,format33)
        # sheet.write(row,0,'BANCO',format33)
        # sheet.write(row,1,'MONEDA',format33)
        # sheet.write(row,2,'IBAN',format33)
        # row+=1
        
        
        # for bank_line in self.env.company.partner_id.bank_ids:
        #     sheet.write(row,0,bank_line.bank_id.name,format43)
        #     sheet.write(row,1,bank_line.currency_id.name,format43)
        #     sheet.write(row,2,bank_line.acc_number,format43)
        #     row+=1
        # self.env.company.partner_id.bank_ids
        
        # sheet.write(row,0,'BAC',format43)
        # sheet.write(row,1,'COL',format43)
        # sheet.write(row,2,'CR59010200009025370183',format43)
        # row+=1
        # sheet.write(row,0,'BAC',format43)
        # sheet.write(row,1,'DOL',format43)
        # sheet.write(row,2,'CR81010200009025370757',format43)
        # row+=1
        # sheet.write(row,0,'BNCR',format43)
        # sheet.write(row,1,'COL',format43)
        # sheet.write(row,2,'CR09015104210010001211',format43)
        # row+=1
        # sheet.write(row,0,'BNCR',format43)
        # sheet.write(row,1,'DOL',format43)
        # sheet.write(row,2,'CR07015100010026174558',format43)
        # row+=1
        # sheet.write(row,0,'BCR',format43)
        # sheet.write(row,1,'COL',format43)
        # sheet.write(row,2,'CR81015201001013334024',format43)
        # row+=1
        # sheet.write(row,0,'BCR',format43)
        # sheet.write(row,1,'DOL',format43)
        # sheet.write(row,2,'CR74015201001013334538',format43)
        
        row+=2
        sheet.write(row,0,'Notificaciones de Pago:',format51)
        
        
        
        mail = ''
        employee_ids = self.env['hr.employee'].browse(data['employee_ids'])
        # raise ValidationError('esta es la data=========>%s' %employee_id.work_email)
        mail = ''
        for emp in employee_ids:
            mail += (emp.work_email+',') if  emp.work_email else ' '
        
        sheet.write(row,1, mail ,format52)
        
        