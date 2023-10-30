# -*- coding: utf-8 -*-

{
    'name': 'BrainPack Push Notifications Enhancement',
    'category': 'Social',
    'summary': 'Send Push notifications to your Mobile App.',
    'version': '16.0.0.0',
    'description': """Send Push notifications to your Mobile App""",
    'depends': ['mail','brainpack_mobile_app'],
    'author': 'BrainPack',
    'website': 'https://www.brainpack.io',
    'external_dependencies': {
        'python': ['firebase_admin'],
    },
    'data': [
        'views/res_users_view.xml',
        'data/notifications_data.xml',
        'views/push_account_view.xml',
        'views/push_notification_view.xml',
        'security/ir.model.access.csv',
    ],
}
