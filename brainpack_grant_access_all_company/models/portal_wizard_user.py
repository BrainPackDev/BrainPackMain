from odoo import api, fields, models, Command
from odoo.tools import email_normalize

class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    re_invite_disable = fields.Boolean("Invite Disable",default=False)

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

    # def action_invite_again(self):
    #     self.write({'re_invite_disable':True})
    #     return super().action_invite_again()


    def action_grant_access(self):
        action = self.env.ref('brainpack_grant_access_all_company.assign_company_wizard_action')
        result = action.read()[0]
        result.update({
            'context':{
                'default_company_id':self.env.company.id,
                'default_portal_wizard_user_id':self.id,
            }
        })
        return result

    def action_invite_again(self):
        self.ensure_one()
        action = self.env.ref('brainpack_grant_access_all_company.assign_company_wizard_action_re_invite')
        result = action.read()[0]
        result.update({
            'context': {
                'default_company_id': self.env.company.id,
                'default_portal_wizard_user_id': self.id,
            }
        })
        return result


