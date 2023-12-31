# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details
{
    'name': 'BrainPack Backend Enterprise Theme',
    'category': 'Themes/Backend',
    'version': '16.0.0.5',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'summary': 'The ultimate Odoo Backend theme with the most advanced key features of all time. Get your own personalized view while working on the Backend system with a wide range of choices. BrainPack theme has 3 in 1 Theme Style, Progressive Web App, Fully Responsive for all apps, Configurable Apps Icon, App Drawer with global search, RTL & Multi-Language Support, and many other key features.',
    'description': """ The ultimate Odoo Backend theme with the most advanced key features of all time. Get your own personalized view while working on the Backend system with a wide range of choices. BrainPack theme has 3 in 1 Theme Style, Progressive Web App, Fully Responsive for all apps, Configurable Apps Icon, App Drawer with global search, RTL & Multi-Language Support, and many other key features. """,
    'depends': ['web', 'base_setup', 'portal', 'resource','brainpack_debranding','brainpack_access_rights'],
    'data': [
        'security/ir.model.access.csv',
        'data/backend_config_data.xml',
        'data/global_level_config.xml',
        'views/manifest.xml',
        'views/pwa_offline.xml',

        'views/backend_configurator_view.xml',
        'views/res_users_view.xml',
        'views/ir_module_view.xml',
        'views/pwa_shortcuts_view.xml',
        'views/res_config_setting.xml',

        'views/menuitems.xml',

        'views/backend_configurator_template.xml',
        'views/login_page_style.xml',
        'views/templates_inherit.xml',
        'views/to_do_list_template.xml',
    ],
    'demo': [
        'data/brain_pack_default_images.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Qweb files
            '/brain_pack_backend_ent/static/src/xml/web_inherit.xml',
            '/brain_pack_backend_ent/static/src/xml/menu.xml',
            '/brain_pack_backend_ent/static/src/xml/bookmark.xml',
            '/brain_pack_backend_ent/static/src/xml/base.xml',
            '/brain_pack_backend_ent/static/src/xml/view_button_icons.xml',
            '/brain_pack_backend_ent/static/src/xml/list_renderer.xml',
            '/brain_pack_backend_ent/static/src/xml/form_statusbar.xml',
            '/brain_pack_backend_ent/static/src/js/widgets/BrainPackDocumentViewer.xml',

            # scss files
            "/brain_pack_backend_ent/static/src/scss/custom_varibles.scss",
            "/brain_pack_backend_ent/static/src/scss/font_icons.scss",
            "/brain_pack_backend_ent/static/src/scss/font-family.scss",

            "/brain_pack_backend_ent/static/src/scss/modal.scss",
            "/brain_pack_backend_ent/static/src/scss/search_modal.scss",
            "/brain_pack_backend_ent/static/src/scss/chat_window.scss",
            "/brain_pack_backend_ent/static/src/scss/common_view.scss",
            "/brain_pack_backend_ent/static/src/scss/discuss_style.scss",
            "/brain_pack_backend_ent/static/src/scss/list_view.scss",
            "/brain_pack_backend_ent/static/src/scss/kanban_view.scss",

            "/brain_pack_backend_ent/static/src/scss/form_view.scss",
            "/brain_pack_backend_ent/static/src/scss/form_chatter.scss",
            "/brain_pack_backend_ent/static/src/scss/tree_form_split_view.scss",

            "/brain_pack_backend_ent/static/src/scss/activity_view.scss",
            "/brain_pack_backend_ent/static/src/scss/pivot_view.scss",
            "/brain_pack_backend_ent/static/src/scss/graph_view.scss",
            "/brain_pack_backend_ent/static/src/scss/dashboards.scss",
            "/brain_pack_backend_ent/static/src/scss/calendear_view.scss",
            "/brain_pack_backend_ent/static/src/scss/setting_page.scss",
            "/brain_pack_backend_ent/static/src/scss/tab_styles.scss",
            "/brain_pack_backend_ent/static/src/scss/popup_styles.scss",
            "/brain_pack_backend_ent/static/src/scss/checkbox_styles.scss",
            "/brain_pack_backend_ent/static/src/scss/radio_styles.scss",
            "/brain_pack_backend_ent/static/src/scss/separator_styles.scss",
            "/brain_pack_backend_ent/static/src/scss/search_panel.scss",
            "/brain_pack_backend_ent/static/src/scss/loader.scss",
            "/brain_pack_backend_ent/static/src/scss/appdrawer.scss",
            "/brain_pack_backend_ent/static/src/scss/bookmarks.scss",
            "/brain_pack_backend_ent/static/src/scss/controlpannel.scss",
            "/brain_pack_backend_ent/static/src/scss/side_menu.scss",
            "/brain_pack_backend_ent/static/src/scss/responsive.scss",
            "/brain_pack_backend_ent/static/src/scss/notification.scss",
            "/brain_pack_backend_ent/static/src/scss/burger_menu.scss",
            "/brain_pack_backend_ent/static/src/scss/website_menu.scss",
            "/brain_pack_backend_ent/static/src/scss/multi_tab.scss",
            "/brain_pack_backend_ent/static/src/scss/to_do_list.scss",
            "/brain_pack_backend_ent/static/src/scss/datetime_pickers.scss",
            "/brain_pack_backend_ent/static/src/css/style.css",

            # js files
            '/brain_pack_backend_ent/static/src/js/widgets/BrainPackDocumentViewer.js',
            "/brain_pack_backend_ent/static/src/js/color_pallet.js",
            "/brain_pack_backend_ent/static/src/js/flip_min.js",
            "/brain_pack_backend_ent/static/src/js/menu.js",
            "/brain_pack_backend_ent/static/src/js/user_menu.js",
            "/brain_pack_backend_ent/static/src/js/apps_menu.js",
            "/brain_pack_backend_ent/static/src/js/SwitchCompanyMenu.js",
            "/brain_pack_backend_ent/static/src/js/form_view_renderer.js",
            "/brain_pack_backend_ent/static/src/js/form_controller.js",
            "/brain_pack_backend_ent/static/src/js/list_view_renderer.js",
            "/brain_pack_backend_ent/static/src/js/BrainPackPageTitle.js",
            "/brain_pack_backend_ent/static/src/js/pwebapp.js",
            "/brain_pack_backend_ent/static/src/js/iconpack_load.js",
            "/brain_pack_backend_ent/static/src/js/action_service.js",
            "/brain_pack_backend_ent/static/src/js/menu_service.js",
            "/brain_pack_backend_ent/static/src/js/dialog.js",
        ],
        'web.assets_frontend': [
            '/brain_pack_backend_ent/static/src/scss/loginpage.scss',
        ],
    },
    # 'live_test_url': 'https://bit.ly/spiffy16',
    'images': [
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'price': 120,
    'license': 'OPL-1',
    'currency': 'EUR',
}
