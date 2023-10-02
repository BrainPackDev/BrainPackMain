# -*- coding: utf-8 -*-

{
    'name': 'Dynamic Financial Reports BrainPack',
    'version': '16.0.1.0.8',
    'category': 'Accounting',
    'summary': """Dynamic Financial Reports with drill 
                down and filters– Community Edition""",
    'description': "Dynamic Financial Reports, DynamicFinancialReports, FinancialReport, Accountingreports, odoo reports, odoo"
                   "This module creates dynamic Accounting General Ledger, Trial Balance, Balance Sheet "
                   "Proft and Loss, Cash Flow Statements, Partner Ledger,"
                   "Partner Ageing, Day book"
                   "Bank book and Cash book reports in Odoo 14 community edition.",
    'author': 'BrainPack',
    'website': "https://www.brainpack.io",
    'company': 'BrainPack',
    'maintainer': 'BrainPack',
    'depends': ['base', 'base_accounting_kit'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        'views/kit_menus.xml',
        'views/reports_config_view.xml',
        'report/trial_balance.xml',
        'report/general_ledger.xml',
        'report/cash_flow_report.xml',
        'report/financial_report_template.xml',
        'report/partner_ledger.xml',
        'report/ageing.xml',
        'report/daybook.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dynamic_accounts_report/static/src/css/report.css',
            'dynamic_accounts_report/static/src/js/action_manager.js',
            'dynamic_accounts_report/static/src/js/general_ledger.js',
            'dynamic_accounts_report/static/src/js/trial_balance.js',
            'dynamic_accounts_report/static/src/js/cash_flow.js',
            'dynamic_accounts_report/static/src/js/financial_reports.js',
            'dynamic_accounts_report/static/src/js/partner_ledger.js',
            'dynamic_accounts_report/static/src/js/ageing.js',
            'dynamic_accounts_report/static/src/js/daybook.js',
            'dynamic_accounts_report/static/src/xml/general_ledger_view.xml',
            'dynamic_accounts_report/static/src/xml/trial_balance_view.xml',
            'dynamic_accounts_report/static/src/xml/cash_flow_view.xml',
            'dynamic_accounts_report/static/src/xml/financial_reports_view.xml',
            'dynamic_accounts_report/static/src/xml/partner_ledger_view.xml',
            'dynamic_accounts_report/static/src/xml/ageing.xml',
            'dynamic_accounts_report/static/src/xml/daybook.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': '_load_account_details_post_init_hook',
    'uninstall_hook': 'unlink_records_financial_report'
}
