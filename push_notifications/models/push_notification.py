# -*- coding: utf-8 -*-

import json
import re

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError
from datetime import datetime

# from pyfcm import FCMNotification
from firebase_admin import messaging
import logging
_logger = logging.getLogger(__name__)


class AppPushNotitfcation(models.Model):
    _name = 'app.push.notification'
    _rec_name = 'app_notification_title'

    message = fields.Text("Message", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent Notification'),
        ('cancel', 'Cancelled'),
        ('fail', 'Fail')],
        string='Status', default='draft', readonly=True, required=True)
    account_ids = fields.Many2one('push.account',
                                   string='Accounts',
                                   help="The accounts on which this post will be published.")

    app_notification_title = fields.Char(string="Notification Title")
    app_notification_image = fields.Char(string="Notification Image (URL)")
    app_notification_icon = fields.Char(string="Notification Icon (URL)")
    notification_send_datetime = fields.Datetime('Notification Send Datetime')
    state_ids = fields.Many2many('res.country.state', string="State")
    # user_type_ids = fields.Many2many('user.type', string="Type")
    # city_ids = fields.Many2many('prozo.city', string="City")
    users_ids = fields.Many2many('res.users', sting="Users", store=True)
    active_users_ids = fields.Many2many('res.users', 'push_notification_active_user_rel', 'active_user_id', 'push_notification_id',sting="Users")
    post_method = fields.Selection([
        ('now', 'Send now'),
        ('scheduled', 'Schedule later')], string="When", default='now', required=True,
        help="Publish your post immediately or schedule it at a later time.")

    scheduled_date = fields.Datetime('Scheduled post date')
    # sale.coupon.program
    # coupon_id = fields.Many2one('sale.coupon.program', string="Coupon", domain=get_coupon_domain)
    # promo_code = fields.Char(string="Promotion Code", related="coupon_id.promo_code")
    failure_count = fields.Integer(string="Failure Count")
    sent_count = fields.Integer(string="Success Count")
    fail_msg = fields.Text(string="Failed Message")
    failed_tokens = fields.Text(string="Failed Tokens")
    is_show_user = fields.Boolean(string="Is Show Users?",default=True)
    total_users = fields.Integer(string="Total Users")
    message_id = fields.Many2one('mail.message')

    @api.model
    def default_get(self, fields):
        res = super(AppPushNotitfcation, self).default_get(fields)
        # res['account_ids'] = [(6, 0 , self.env.ref('push_notifications.social_account_mobile_app').ids )]
        res['account_ids'] =  self.env.ref('push_notifications.social_account_mobile_app').id
        return res


    def push_pyfcm_multi(self, fcm_device_token, data={}):
        account_id = self.env['push.account'].search([('is_mobile_app_notification', '=', True)])
        account_id._init_firebase_app()
        results = []
        firebase_message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=data.get('title'),
                body=data.get('body'),
                image=data.get('image'),
            ),
            tokens=fcm_device_token,
        )
        response = messaging.send_multicast(firebase_message)

        results.append(response)
        self.sent_count = response.success_count
        self.failure_count = response.failure_count
        _logger.info('\n\n{0} messages were sent successfully'.format(response.success_count))
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            self.state = 'fail'
            self.fail_msg = response.responses 
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(fcm_device_token[idx])
            self.failed_tokens = str(failed_tokens)
            _logger.info('List of tokens that caused failures: {0}'.format(failed_tokens))
        else:
            self.state = 'sent'
        if response.success_count > 0:
            self.state = 'sent'
        _logger.info('Successfully sent message:',  results)


    def cancel_notification(self):
        for notifi_id in self:
            notifi_id.state = 'cancel'

    def send_notitfcation(self):
        is_token = True
        fcm_device_token = []
        if not self.users_ids:
            raise UserError(_("Users not selected."))
        for users_id in self.users_ids:
            if not users_id.fcm_token:
                is_token = False
            else:
                fcm_device_token.append(users_id.fcm_token)

        if not is_token:
            raise UserError(_("Token not set on all selected user."))
        sent_now = False
        if self and self.post_method == 'now':
            sent_now = True
        if self and self.post_method == 'scheduled':
            if self.scheduled_date <= fields.Datetime.now() and self.state == 'scheduled':
                sent_now = True
            else: 
                sent_now = False

        if sent_now:

            title = self.app_notification_title and self.app_notification_title or "Test Notitfcation"
            body  = self.message and self.message or "Test Notitfcation" 
            icon = self.app_notification_icon and self.app_notification_icon or ''
            image = self.app_notification_image and self.app_notification_image or ''
            data = {'title':title, 'body':body, 'image': image, 'icon': icon}
            self.notification_send_datetime = fields.Datetime.now()
            self.active_users_ids = [(6, 0, self.users_ids.ids)]
            self.push_pyfcm_multi(fcm_device_token, data)

    @api.model
    def _cron_scheduled_push_notification(self):
        push_notification_ids =  self.search([
            ('post_method', '=', 'scheduled'),
            ('state', '=', 'scheduled'),
            ('scheduled_date', '<=', fields.Datetime.now())
        ])
        for push_notification_id in push_notification_ids:
            push_notification_id.send_notitfcation()
