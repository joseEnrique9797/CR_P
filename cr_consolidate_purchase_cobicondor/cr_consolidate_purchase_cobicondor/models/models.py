# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cr_consolidate_purchase_cobicondor(models.Model):
#     _name = 'cr_consolidate_purchase_cobicondor.cr_consolidate_purchase_cobicondor'
#     _description = 'cr_consolidate_purchase_cobicondor.cr_consolidate_purchase_cobicondor'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
