# -*- coding: utf-8 -*-
# from odoo import http


# class ./crCalculateDaiProduct(http.Controller):
#     @http.route('/./cr_calculate_dai_product/./cr_calculate_dai_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./cr_calculate_dai_product/./cr_calculate_dai_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('./cr_calculate_dai_product.listing', {
#             'root': '/./cr_calculate_dai_product/./cr_calculate_dai_product',
#             'objects': http.request.env['./cr_calculate_dai_product../cr_calculate_dai_product'].search([]),
#         })

#     @http.route('/./cr_calculate_dai_product/./cr_calculate_dai_product/objects/<model("./cr_calculate_dai_product../cr_calculate_dai_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./cr_calculate_dai_product.object', {
#             'object': obj
#         })
