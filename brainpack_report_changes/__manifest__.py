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
    'depends': ['sale','account'],
    'data': [
        'data/report_data.xml',
        'views/res_company.xml',
        'views/ir_actions_report_templates.xml',
        'views/report_invoice.xml',
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