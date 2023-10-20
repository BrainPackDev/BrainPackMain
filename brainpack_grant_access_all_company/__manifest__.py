{
    'name': 'BrainPack Grant Portal Access Custom',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['portal'],
    'data': [
        'data/mail_template_data.xml',
        'views/assign_company.xml',
        'views/portal_wizard_views.xml',
        'views/res_config_settings.xml',
        'security/ir.model.access.csv',
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