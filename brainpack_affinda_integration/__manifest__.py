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
    'depends': ['contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/affinda_organization.xml',
        'views/affinda_workspace.xml',
        'views/affinda_workspace_collection.xml',
        'views/affinda_document.xml',
        'views/res_config_setting.xml',
    ],
    'assets': {
        'web.assets_backend': [

        ],
    },

}
