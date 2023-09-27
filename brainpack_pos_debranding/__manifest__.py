{
    'name': 'BrainPack Pos Debranding',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['point_of_sale','brainpack_debranding'],
    'data': [
        'views/app_theme_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'brainpack_pos_debranding/static/src/css/pos.css',
            'brainpack_pos_debranding/static/src/xml/Chrome.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}