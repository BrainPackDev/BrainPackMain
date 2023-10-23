{
    'name': 'BrainPack Appointments',
    'version': '1.0',
    'category': 'BrainPack Marketing/Online Appointment',
    'summary': 'BrainPack Allow people to book meetings in your agenda',
    'website': 'https://www.brainpack.io',
    'description': """
        BrainPack Allow clients to Schedule Appointments through the Portal
    """,
    'depends': ['calendar', 'onboarding', 'portal'],
    'data': [
        'data/onboarding_data.xml',
        'data/calendar_data.xml',
        'data/mail_message_subtype_data.xml',
        'data/mail_template_data.xml',
        'views/calendar_views.xml',
        'views/calendar_alarm_views.xml',
        'views/calendar_event_views.xml',
        'views/appointment_answer_input_views.xml',
        'views/appointment_invite_views.xml',
        'views/appointment_question_views.xml',
        'views/appointment_type_views.xml',
        'views/appointment_slot_views.xml',
        'views/calendar_menus.xml',
        'views/appointment_templates_appointments.xml',
        'views/appointment_templates_registration.xml',
        'views/appointment_templates_validation.xml',
        'views/portal_templates.xml',
        'wizard/appointment_onboarding_link.xml',
        'security/calendar_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'data/res_partner_demo.xml',
        'data/appointment_demo.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web_editor.assets_wysiwyg': [
            'brainpack_appointment/static/src/js/wysiwyg.js',
        ],
        'web.assets_frontend': [
            'brainpack_appointment/static/src/scss/appointment.scss',
            'brainpack_appointment/static/src/js/appointment_select_appointment_type.js',
            'brainpack_appointment/static/src/js/appointment_select_appointment_slot.js',
            'brainpack_appointment/static/src/xml/appointment_svg.xml',
            'brainpack_appointment/static/src/js/appointment_form.js',
            'brainpack_appointment/static/src/xml/appointment_slots.xml',
            'brainpack_appointment/static/src/xml/appointment_svg.xml',
            'brainpack_appointment/static/src/xml/appointment_no_slot.xml',
        ],
        'web.assets_backend': [
            'brainpack_appointment/static/src/css/style.css',
            'brainpack_appointment/static/src/scss/appointment_type_views.scss',
            'brainpack_appointment/static/src/scss/web_calendar.scss',
            'brainpack_appointment/static/src/js/appointment_invite_form_renderer.js',
            'brainpack_appointment/static/src/js/appointment_invite_form_views.js',
            'brainpack_appointment/static/src/views/**/*',
        ],
        'web_studio.studio_assets': [
            'brainpack_appointment/static/src/scss/legacy_appointment_type_views.scss',
        ],
        'web.qunit_suite_tests': [
            'brainpack_appointment/static/tests/*',
        ],
    }
}
