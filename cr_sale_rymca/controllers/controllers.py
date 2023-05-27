# -*- coding: utf-8 -*-
# from odoo import http


# class CrSaleRymca(http.Controller):
#     @http.route('/cr_sale_rymca/cr_sale_rymca/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cr_sale_rymca/cr_sale_rymca/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cr_sale_rymca.listing', {
#             'root': '/cr_sale_rymca/cr_sale_rymca',
#             'objects': http.request.env['cr_sale_rymca.cr_sale_rymca'].search([]),
#         })

#     @http.route('/cr_sale_rymca/cr_sale_rymca/objects/<model("cr_sale_rymca.cr_sale_rymca"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cr_sale_rymca.object', {
#             'object': obj
#         })
