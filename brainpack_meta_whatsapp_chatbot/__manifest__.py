{
    'name': 'Brainpack Meta Whatsapp ChatBot',
    'version': '16.0',
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'category': 'Base',
    'summary': 'Interactive Templates, Buttons send through brainpack on WhatsApp and Message Automation',
    'description': """
        Interactive Templates, Buttons send through odoo on WhatsApp and Message Automation
    """,
    'depends': ['brainpack_meta_whatsapp'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/components.xml',
        # 'views/interactive_list_views.xml',
        # 'views/interactive_product_list_views.xml',
        'views/whatsapp_chatbot_script_views.xml',
        'views/mail_channel_views.xml',
        'views/whatsapp_chatbot_views.xml',
        # 'views/wa_template_views_inherit.xml',
        'views/whatsapp_ir_action_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/brainpack_meta_whatsapp_chatbot/static/src/scss/kanban_view.scss'
            ],
    },
    'installable': True,
    'auto_install': False,
}