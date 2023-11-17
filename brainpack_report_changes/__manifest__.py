{
    'name': 'BrainPack Report Changes',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['sale','account','sale_subscription'],
    'data': [
        'data/report_data.xml',
        'data/mail_template.xml',
        'views/res_company.xml',
        'views/ir_actions_report_templates.xml',
        'views/report_invoice.xml',
        'views/sale_portal.xml',
        'views/subscription_portal_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}