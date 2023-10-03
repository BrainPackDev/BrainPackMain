import logging

from odoo import models, fields, api
from odoo.tools import populate, groupby

_logger = logging.getLogger(__name__)


class ProjectProjectInherit(models.Model):
    _inherit = "project.project"

    tracking_emails_cou = fields.Integer(
        compute="_compute_tracking_emails_cou"
    )

    @api.depends('partner_id','partner_id.email')
    def _compute_tracking_emails_cou(self):
        self.tracking_emails_cou = 0
        for rec in self:
            partners_mail = rec.partner_id.filtered("email")
            mt_obj = self.env["mail.tracking.email"].sudo()
            tracking_emails_count = 0
            for partner in partners_mail:
                tracking_emails_count = tracking_emails_count + len(
                    mt_obj.search([("recipient_address", "=", partner.email.lower())])
                )
            rec.tracking_emails_cou = tracking_emails_count

    def open_mail_tracking_form(self):
        partners_mail = self.partner_id.filtered("email")
        mt_obj = self.env["mail.tracking.email"].sudo()
        if partners_mail:
            mt_obj = mt_obj.search(
                [("recipient_address", "=", partners_mail.email.lower())])
        return {
            'name': ('MailTracking emails'),
            'view_mode': 'tree,form',
            'target': 'current',
            'res_model': 'mail.tracking.email',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', mt_obj.ids)],
            'context': {
            }
        }