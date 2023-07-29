# -*- coding: utf-8 -*-
# from odoo import http


# class CrConsolidatePurchaseCobicondor(http.Controller):
#     @http.route('/cr_consolidate_purchase_cobicondor/cr_consolidate_purchase_cobicondor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cr_consolidate_purchase_cobicondor/cr_consolidate_purchase_cobicondor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cr_consolidate_purchase_cobicondor.listing', {
#             'root': '/cr_consolidate_purchase_cobicondor/cr_consolidate_purchase_cobicondor',
#             'objects': http.request.env['cr_consolidate_purchase_cobicondor.cr_consolidate_purchase_cobicondor'].search([]),
#         })

#     @http.route('/cr_consolidate_purchase_cobicondor/cr_consolidate_purchase_cobicondor/objects/<model("cr_consolidate_purchase_cobicondor.cr_consolidate_purchase_cobicondor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cr_consolidate_purchase_cobicondor.object', {
#             'object': obj
#         })
