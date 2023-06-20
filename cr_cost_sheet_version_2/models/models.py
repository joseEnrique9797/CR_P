# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cr_cost_sheet_version_2(models.Model):
#     _name = 'cr_cost_sheet_version_2.cr_cost_sheet_version_2'
#     _description = 'cr_cost_sheet_version_2.cr_cost_sheet_version_2'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
