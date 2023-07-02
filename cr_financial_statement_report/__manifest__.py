# -*- coding: utf-8 -*-
{
    'name': "Financial Statement Report",

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
    'depends': ['base','report_xlsx','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'views/res_partner.xml',
        'views/res_company.xml',
        # 'views/res_config_settings_views.xml',
        'report/financial_statement_report_pdf.xml',
        'data/res_partner_server_actions.xml',
        'wizard/financial_statement_wizard.xml',
        'report/financial_statement_report_xlsx.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
