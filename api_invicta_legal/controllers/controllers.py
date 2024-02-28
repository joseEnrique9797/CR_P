# -*- coding: utf-8 -*-
from odoo import http
import requests
import logging

_logger = logging.getLogger(__name__)

class ApiInvictaLegal(http.Controller):
    @http.route('/api_invicta_legal/endPoint_payment', auth='public')
    def endPoint_payment(self, **kw):

        url = "https://invictalegal.thetimebilling.com/time_tracking/api/v2/login"
        payload = {
            "user": "integraciones@lemontech.com",
            "password": "Lemontech24",
            "app_key": "odoocr"
        }
        
        response = requests.post(url, json=payload)
        _logger.info('This is an info response 222 @@@@@@@@@@@@@@@@@ %s' %(response.text))
        if response.status_code == 200 and response.text.strip():
            return response.json()
        else:
            return "No JSON content in response"
        





        # url = "https://ambiente.thetimebilling.com/api/v2/clients"
        # headers = {
        #     "AUTHTOKEN": "<auth_token>",
        # }
        # return "Hello, world"
        # response = requests.get(url, headers=headers)
        # return response.json()
#     @http.route('/api_invicta_legal/api_invicta_legal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('api_invicta_legal.listing', {
#             'root': '/api_invicta_legal/api_invicta_legal',
#             'objects': http.request.env['api_invicta_legal.api_invicta_legal'].search([]),
#         })

#     @http.route('/api_invicta_legal/api_invicta_legal/objects/<model("api_invicta_legal.api_invicta_legal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('api_invicta_legal.object', {
#             'object': obj
#         })
