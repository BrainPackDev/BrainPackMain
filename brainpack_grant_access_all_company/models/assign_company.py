from odoo import api, fields, models, Command
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import email_normalize

class AssignCompany(models.TransientModel):
    _name = 'assign.company'

    company_id = fields.Many2one('res.company',string="Company")
    portal_wizard_user_id = fields.Many2one('portal.wizard.user')

    def action_grant_access(self):
        self.ensure_one()
        portal_user = self.portal_wizard_user_id
        portal_user._assert_user_email_uniqueness()

        if portal_user.is_portal or portal_user.is_internal:
            raise UserError(_('The partner "%s" already has the portal access.', portal_user.partner_id.name))

        group_portal = self.env.ref('base.group_portal')
        group_public = self.env.ref('base.group_public')

        portal_user._update_partner_email()
        user_sudo = portal_user.user_id.sudo()

        if not user_sudo:
            # create a user if necessary and make sure it is in the portal group
            # company = portal_user.partner_id.company_id or self.env.company
            company = self.company_id
            user_sudo = portal_user.sudo().with_company(company.id)._create_user()

        if not user_sudo.active or not portal_user.is_portal:
            user_sudo.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_public.id)]})
            # prepare for the signup process
            user_sudo.partner_id.signup_prepare()

        portal_user.with_context(active_test=True)._send_email()

        return portal_user.action_refresh_modal()

    def action_invite_again(self):
        self.ensure_one()
        portal_user = self.portal_wizard_user_id
        if portal_user.user_id:
            portal_user.user_id.sudo().write({'company_id':self.company_id.id})

        portal_user.write({'re_invite_disable': True})
        portal_user._assert_user_email_uniqueness()

        if not portal_user.is_portal:
            raise UserError(_('You should first grant the portal access to the partner "%s".', portal_user.partner_id.name))

        portal_user._update_partner_email()
        portal_user.with_context(active_test=True)._send_email()

        return portal_user.action_refresh_modal()