{
    "name": "Resource booking",
    "summary": "Manage appointments and resource booking",
    "version": "16.0.1.2.1",
    "development_status": "Production/Stable",
    "category": "Appointments",
    "website": "https://www.brainpack.io",
    "author": "BrainPack",
    "maintainers": ["BrainPack"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "external_dependencies": {
        "python": [
            # Used implicitly
            "cssselect",
        ],
    },
    "depends": [
        "calendar",
        "mail",
        "portal",
        "resource",
        "web_calendar_slot_duration",
    ],
    "data": [
        "data/mail.xml",
        "security/resource_booking_security.xml",
        "security/ir.model.access.csv",
        "templates/portal.xml",
        "views/calendar_event_views.xml",
        "views/resource_booking_combination_views.xml",
        "views/resource_booking_type_views.xml",
        "views/resource_booking_views.xml",
        "views/menus.xml",
    ],
    "assets": {
        "web.assets_frontend": ["resource_booking/static/src/scss/portal.scss"],
        "web.assets_tests": ["resource_booking/static/src/js/resource_booking_tour.js"],
    },
    "demo": ["demo/res_users_demo.xml"],
}
