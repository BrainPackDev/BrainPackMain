# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Website Image Hotspot Snippet",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Website",
    "license": "OPL-1",
    "summary": "Image Hotspot On Image Hotspots Custom Hotspot Responsive Image Hotspot In Image With Multiple Hotspot Create Image Hotspot Popover Link Information With Image Link Products In Hotspot Own Hotspot Odoo",
    "description": """This module allows you to show the hotspot on the images on the website. You can link products using a hotspot that improves your marketing. Image hotspot helps to link multiple information on the same image which is visible when hover on the hotspot. We provide 5 predefine hotspot popover styles as well you can modify hotspot popover style. You can create your own hotspot style also. You can use this snippet without any technical skill.""",
    "version": "16.0.1",
    "depends": ['website'],
    'data': [
        "security/ir.model.access.csv",
        "data/sh_hotspot_snippet_demo.xml",
        "views/sh_image_hotpost_info_views.xml",
        "views/sh_image_snippet_templates.xml",
        "views/website_templates.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "sh_image_hotspot_snippet/static/src/scss/style.scss",
            "sh_image_hotspot_snippet/static/src/js/frontend.js",
            "sh_image_hotspot_snippet/static/src/js/custom.js",
        ],
        # 'website.assets_editor': [
        #
        # ],
        'website.assets_wysiwyg': [
            "sh_image_hotspot_snippet/data/sh_hotspot_snippet_demo.xml",
            "sh_image_hotspot_snippet/static/src/js/image_hotspot.js",
        ],

    },
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/background.gif", ],
    "price": 50,
    "currency": "EUR"
}
