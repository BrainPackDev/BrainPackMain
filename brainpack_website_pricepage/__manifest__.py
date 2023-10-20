{
    'name': 'BrainPack Website PricePage',
    'version': '16.0.0.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'license': 'LGPL-3',
    'sequence': 2,
    'images': [],
    'summary': """
    """,
    'depends': ['website'],
    'data': [
        'views/bpprice.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/brainpack_website_pricepage/static/src/js/price.js',
            '/brainpack_website_pricepage/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'description': """
    """,
}