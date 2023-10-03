from odoo import _, api, fields, models, tools


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        mail_template = self.env.ref('brainpack_helpdesk_mgmt.mail_template_create_ticket_mail').id
        template = self.env['mail.template'].browse(mail_template)
        template.send_mail(res.id, force_send=True)
        return res
