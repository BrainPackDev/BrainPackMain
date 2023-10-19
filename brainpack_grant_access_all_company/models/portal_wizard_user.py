from odoo import api, fields, models, Command
from odoo.tools import email_normalize

class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    def _create_user(self):
        company_ids = [com.get('id') for com in self.env['res.company'].sudo().search_read([],['id'])]
        if not company_ids:
            company_ids = self.env.company.ids
        return self.env['res.users'].with_context(no_reset_password=True)._create_user_from_template({
            'email': email_normalize(self.email),
            'login': email_normalize(self.email),
            'partner_id': self.partner_id.id,
            'company_id': self.env.company.id,
            'company_ids': [(6, 0, company_ids)],
        })