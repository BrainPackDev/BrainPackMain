# -*- coding: utf-8 -*-
{
    'name': "BrainPack Affinda Integration",

    'summary': """
      """,

    'author': "BrainPack",
    'website': "https://www.brainpack.io",
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts','account','hr_expense'],

    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/affinda_organization.xml',
        'views/affinda_workspace.xml',
        'views/affinda_workspace_collection.xml',
        'views/affinda_document.xml',
        'views/res_config_setting.xml',
        'views/res_partner.xml',
        'views/hr_expense.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'brainpack_affinda_integration/static/src/xml/review_url_iframe.xml',
            'brainpack_affinda_integration/static/src/css/style.css',
            'brainpack_affinda_integration/static/src/js/review_url_iframe.js',
        ],
    },
}
