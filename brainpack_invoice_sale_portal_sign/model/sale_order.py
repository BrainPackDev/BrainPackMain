from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sign_company_name = fields.Char('Company Name')
    sign_company_number = fields.Char('Company Number')
    behalf_of_company = fields.Boolean('Sign Behalf Of Company')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if not self.signature:
            mail_template = self.env.ref('brainpack_invoice_sale_portal_sign.mail_template_sale_confirmation_sign').id
            template = self.env['mail.template'].browse(mail_template)
            template.send_mail(self.id, force_send=True)
        return res
