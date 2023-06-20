# -*- coding: utf-8 -*-
# from odoo import http


# class CrCostSheetVersion2(http.Controller):
#     @http.route('/cr_cost_sheet_version_2/cr_cost_sheet_version_2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cr_cost_sheet_version_2/cr_cost_sheet_version_2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cr_cost_sheet_version_2.listing', {
#             'root': '/cr_cost_sheet_version_2/cr_cost_sheet_version_2',
#             'objects': http.request.env['cr_cost_sheet_version_2.cr_cost_sheet_version_2'].search([]),
#         })

#     @http.route('/cr_cost_sheet_version_2/cr_cost_sheet_version_2/objects/<model("cr_cost_sheet_version_2.cr_cost_sheet_version_2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cr_cost_sheet_version_2.object', {
#             'object': obj
#         })
