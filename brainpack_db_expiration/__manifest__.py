# -*- coding: utf-8 -*-
{
    'name': "BrainPack DB Expiration",

    'summary': """
      """,

    'author': "BrainPack",
    'website': "https://www.brainpack.io",
    'category': 'Uncategorized',
    'version': '16.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['web','brain_pack_backend_ent'],

    'data': [

    ],
    'assets': {
        'web.assets_backend': [
            '/brainpack_db_expiration/static/src/xml/menu.xml',
            '/brainpack_db_expiration/static/src/js/apps_menu.js',
        ],
    },

}
