# -*- coding: utf-8 -*-
from odoo import http
import requests
import logging
from odoo.http import request, Response, content_disposition

_logger = logging.getLogger(__name__)

class ApiInvictaLegal(http.Controller):

    @http.route('/api_invicta_legal/endPointInsertClients', auth='public')
    def endPoint_insert_clients(self, **kw):

        loginParams = self.login()
        
        url = "https://invictalegal.sandbox.thetimebilling.com/time_tracking/api/v2/clients"
        headers = {
            "authToken":  loginParams['auth_token']
        }
        
        response = requests.get(url, headers=headers)

        partner = request.env['res.partner']

        if response.status_code == 200 and response.text.strip():
            for client in response.json():
                
                
                partner_exist = partner.search([
                    ('external_id', '=', client['id'] )
                ])

                _logger.info('func endPoint_insert_clients ============= %s' %(partner_exist))

                if not partner_exist:
                    vals = {
                        'name':client['name'],
                        'external_id':client['id'],
                    }
    
                    partner.sudo().create(vals)

                
        

    
    def login(self):
        url = "https://invictalegal.sandbox.thetimebilling.com/time_tracking/api/v2/login"
        payload = {
            "user": "integraciones@lemontech.com",
            "password": "Lemontech24*",
            "app_key": "odoocr"
        }
        
        response = requests.post(url, json=payload)
        _logger.info('func login  @@@@@@@@@@@@@@@@@ %s' %(response.text))

        if response.status_code == 200 and response.text.strip():
            return response.json()
        
    
    @http.route('/api_invicta_legal/endPoint_payment', auth='public')
    def endPoint_payment(self, **kw):
        url = 'https://invictalegal.sandbox.thetimebilling.com/time_tracking/api/v2/payments'
        loginParams = self.login()
        headers = {
            "authToken":  loginParams['auth_token']
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200 and response.text.strip():
            payment_obj = request.env['account.payment']
            for payment in response.json():
                _logger.info('pagos 3333  @@@@@@@@@@@@@@@@@ %s' %(payment))
                # amount
                partner_exist = request.env['res.partner'].search([
                    ('external_id', '=', payment['client_id'] )
                ])
                if partner_exist:
                    vals = {
                        'date':payment['date'],
                        'amount':payment['amount'],
                        'partner_id':partner_exist.id,
                        'payment_type':'inbound',
                        'external_id':payment['id'],
                    }

                    payment_obj.create(vals)

                    
                
                
                
                break
                


