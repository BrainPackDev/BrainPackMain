# -*- coding: utf-8 -*-

{
    'name': 'Subscriptions',
    'version': '1.1',
    'category': 'Sales/Subscriptions',
    'sequence': 115,
    'summary': 'Generate recurring invoices and manage renewals',
    'description': """
This module allows you to manage subscriptions.

Features:
    - Create & edit subscriptions
    - Modify subscriptions with sales orders
    - Generate invoice automatically at fixed intervals
""",
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'depends': [
        'sale_management',
        'portal',
        'web_cohort',
        'rating',
        'base_automation',
        'sms',
        'sale_temporal',
    ],
    'data': [
        'security/sale_subscription_security.xml',
        'security/ir.model.access.csv',
        'wizard/sale_subscription_close_reason_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/sale_subscription_views.xml',
        'views/res_partner_views.xml',
        'views/account_analytic_account_views.xml',
        'views/subscription_portal_templates.xml',
        'views/subscription_templates.xml',
        'views/payment_templates.xml',
        'views/mail_activity_views.xml',
        'data/mail_template_data.xml',
        'data/sale_subscription_data.xml',
        'data/sms_template_data.xml',
        'report/sale_subscription_report_view.xml',
    ],
    'demo': [
        'data/sale_subscription_demo.xml'
    ],
    'application': True,
    'pre_init_hook': '_pre_init_sale_subscription',
    'assets': {
        'web.assets_backend': [
            'sale_subscription/static/src/js/tours/sale_subscription.js',
        ],
        'web.assets_frontend': [
            'sale_subscription/static/src/js/manage_form.js',
            'sale_subscription/static/src/js/portal_subscription.js',
        ],
    }
}
