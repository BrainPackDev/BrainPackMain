# -*- coding: utf-8 -*-

import logging

from werkzeug.urls import url_join

from odoo import _, fields, models
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError

MISSING_FIREBASE_LIB_ERROR_MESSAGE = """Push Notifications require the `firebase_admin` Python library (version >=2.17.0).
    You need to install it on your system to be able to use this module."""

_logger = logging.getLogger(__name__)
try:
    import firebase_admin
    from firebase_admin import messaging
    from firebase_admin import credentials
except ImportError:
    _logger.warning(MISSING_FIREBASE_LIB_ERROR_MESSAGE)
    firebase_admin = None

class AccountPushNotifications(models.Model):
    _name = 'push.account'

    name = fields.Char(string="Name")
    is_mobile_app_notification = fields.Boolean(string="Is Mobile App Notification?", default=False)
    app_firebase_use_own_account = fields.Boolean('Use your own Firebase account')
    app_firebase_project_id = fields.Char('Project ID')
    app_firebase_web_api_key = fields.Char('Web API Key')
    app_firebase_push_certificate_key = fields.Char('Push Certificate Key')
    app_firebase_sender_id = fields.Char('Sender ID')
    app_firebase_admin_key_file = fields.Many2one('ir.attachment',string='Admin Key')
    # app_firebase_admin_key_file = fields.Binary('Firebase Admin Key File')


    def _compute_stats_link(self):
        """ External link to this Facebook Page's 'insights' (fancy name for the page statistics). """
        res = super(AccountPushNotifications, self )._compute_stats_link()

        if self.is_mobile_app_notification:
            self.stats_link = "https://firebase.google.com/"
        return res
   
    def _check_firebase_version(self):
        """ Utility method to check that the installed firebase version has needed features. """
        version_compliant = firebase_admin and messaging and credentials \
            and hasattr(firebase_admin, 'initialize_app') \
            and hasattr(messaging, 'send')

        if not version_compliant:
            raise UserError(_(MISSING_FIREBASE_LIB_ERROR_MESSAGE))

    def _init_firebase_app(self):
        self.ensure_one()
        if self.is_mobile_app_notification:
            self._check_firebase_version()
            if not self.app_firebase_admin_key_file:
                raise UserError(_("Firebase Admin Key File is missing from the configuration."))

            firebase_credentials = credentials.Certificate(
                self.app_firebase_admin_key_file._full_path(self.app_firebase_admin_key_file.store_fname)
            )
            try:
                firebase_admin.initialize_app(firebase_credentials)
            except ValueError:
                # app already initialized
                pass
        else:
            super(AccountPushNotifications, self)._init_firebase_app()