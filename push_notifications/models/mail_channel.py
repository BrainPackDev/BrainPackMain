import requests
from odoo import api, fields, models
from odoo.addons.web_editor.models.ir_qweb_fields import html_to_text
import html2text

class Channel(models.Model):
    _inherit = "mail.channel"

    def _channel_message_notifications(self, message, message_format=False):
        """Generate the bus notifications for the given message
        :param message : the mail.message to sent
        :returns list of bus notifications (tuple (bus_channe, message_content))
        """
        res = super()._channel_message_notifications(
            message, message_format=message_format
        )

        partners =  self.channel_partner_ids.ids
        if message.author_id and message.author_id.id in partners:
            partners.remove(message.author_id.id)
        if partners:
            domain= []
            domain.append(('partner_id', 'in', partners))
            domain.append(('fcm_token', '!=', False))

            if domain:
                user_ids = self.env['res.users'].sudo().search(domain)
            if user_ids:
                notification_vals = {
                    'message_id': message.id,
                    'app_notification_title': message.author_id.name,
                    'message': html2text.html2text(message.body),
                    'users_ids': [(6,0,user_ids.ids)],
                    'total_users':len(user_ids.ids),
                    'post_method': 'now'
                }
                if message.attachment_ids:
                    notification_vals.update({'message':notification_vals.get('message') + "\n" + ", ".join([attachment.name for attachment in message.attachment_ids])})

                notification = self.env['app.push.notification'].sudo().create(notification_vals)
                notification.send_notitfcation()

        return res