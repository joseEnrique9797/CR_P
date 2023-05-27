# -*- coding: utf-8 -*-
# from odoo import http


# class CrFinancialStatementReport(http.Controller):
#     @http.route('/cr_financial_statement_report/cr_financial_statement_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cr_financial_statement_report/cr_financial_statement_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cr_financial_statement_report.listing', {
#             'root': '/cr_financial_statement_report/cr_financial_statement_report',
#             'objects': http.request.env['cr_financial_statement_report.cr_financial_statement_report'].search([]),
#         })

#     @http.route('/cr_financial_statement_report/cr_financial_statement_report/objects/<model("cr_financial_statement_report.cr_financial_statement_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cr_financial_statement_report.object', {
#             'object': obj
#         })
