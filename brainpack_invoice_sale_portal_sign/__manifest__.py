# -*- coding: utf-8 -*-
{
    'name': 'Brainpack Sale Invoice Portal Sign',
    'version': '16.0.2',
    'category': 'website',
    'summary': 'Sign button inside portal when payment is paid',
    'description': """-----""",
    'website': 'https://www.brainpack.io',
    'author': 'BrainPack',
    'depends': ['website', 'portal', 'account_payment', 'account', 'sale', 'mail', 'payment'],
    'data': ['views/account_portal_template_inherit.xml',
             'views/account_move_view_inherit.xml',
             'views/invoice_report_inherit.xml',
             'views/sale_portal_template_inherit.xml',
             'views/invoice_signature_mail_template.xml',
             'views/sale_order_confirmation_mail_template_inherit.xml',
             ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
