from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    try_demo = fields.Boolean(string='Try Demo',default=False)

    @api.model
    def create(self, vals):
        res = super().create(vals)
        print(">>>>>>>>>>",vals)
        if res.try_demo and res.type == 'lead':
            mail_template = self.env.ref('brainpack_demo_form.mail_template_create_demo_mail_template').id
            template = self.env['mail.template'].browse(mail_template)
            template.send_mail(res.id, force_send=True)
        return res