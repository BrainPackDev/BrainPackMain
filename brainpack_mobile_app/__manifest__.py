{
    'name': 'BrainPack Mobile App',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'description': """
        This module is developed for API.
    """,
    'depends': ['base','website'],
    'data': [
        'security/ir.model.access.csv',
        'data/default_webservice.xml',
        'views/webservice.xml',
        'views/res_config.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}