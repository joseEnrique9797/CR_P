# -*- coding: utf-8 -*-
{
    'name': "cr_cost_sheet_version_2",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'bi_odoo_job_costing_management', 'bi_material_purchase_requisitions' ,'bi_material_requisition_cost_sheet', 'stock'],

    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/job_cost_sheet.xml',
        'views/stock_picking.xml',
        'report/report_sheet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
