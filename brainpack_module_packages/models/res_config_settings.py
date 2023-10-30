from odoo import api, fields, models,_


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_brainpack_db_expiration = fields.Boolean("DB Expiration")
    module_brainpack_hr_access_rights = fields.Boolean("Hr Access Rights")
    module_brainpack_hr_expense_extended = fields.Boolean("Hr Expense Debranding")
    module_brainpack_website_extended = fields.Boolean("Website Extended")
    module_website_helpdesk_mgmt = fields.Boolean("Website Helpdesk Management")
    module_helpdesk_mgmt = fields.Boolean("Helpdesk Management")
    module_mail_tracking = fields.Boolean("Mail Tracking")
    module_project_timesheet_time_control = fields.Boolean("Project Timesheet Time Control")
    module_brain_mail_multicompany = fields.Boolean("Email Gateway Multi company")
    module_brainpack_im_livechat = fields.Boolean("BrainPack Live Chat")
    module_brainpack_invoice_sale_portal_sign = fields.Boolean("Brainpack Sale Invoice Portal Sign")
    module_brainpack_mass_mailing_extended = fields.Boolean("BrainPack Mass Mailing Extended")
    module_brainpack_logo_on_login = fields.Boolean("BrainPack Logo on Login")
    module_brainpack_debranding = fields.Boolean("BrainPack Base")
    module_brain_pack_backend_ent = fields.Boolean("Backend Enterprise Theme")
    module_brainpack_crm_utm_extended = fields.Boolean("UTM Package")


    module_brainpack_meta_whatsapp_chatbot = fields.Boolean("Whatsapp Chatbot")
    module_brainpack_meta_whatsapp_marketing = fields.Boolean("Whatsapp Marketing")
    module_brainpack_meta_whatsapp_discuss = fields.Boolean("Whatsapp Discuss")
    module_brainpack_meta_whatsapp = fields.Boolean("Meta Whatsapp Base")
    module_brainpack_discuss_search_view_cr = fields.Boolean("Discuss Search")
    module_base_account_budget = fields.Boolean("Base Account budget")
    module_dynamic_accounts_report = fields.Boolean("Dynamic Account Report")
    module_base_accounting_kit = fields.Boolean("Base Accounting Kit")

    module_sale_subscription = fields.Boolean("Sale Subscription")

    module_brainpack_pos_debranding = fields.Boolean('POS Debranding')

    @api.onchange('module_brainpack_crm_utm_extended')
    def on_module_brainpack_crm_utm_extended(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_crm_utm_extended'.replace("module_", ''))])
        if not modules and self.module_brainpack_crm_utm_extended:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack UTM Pack modile not exist!'),
                }
            }
    @api.onchange('module_brainpack_pos_debranding')
    def on_module_brainpack_pos_debranding(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_pos_debranding'.replace("module_", ''))])
        if not modules and self.module_brainpack_pos_debranding:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Pos Debranding module not exist!'),
                }
            }

    @api.onchange('module_sale_subscription')
    def on_module_sale_subscription(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_sale_subscription'.replace("module_", ''))])
        if not modules and self.module_sale_subscription:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Subscriptions module not exist!'),
                }
            }

    @api.onchange('module_base_accounting_kit')
    def on_module_base_accounting_kit(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_base_accounting_kit'.replace("module_", ''))])
        if not modules and self.module_base_accounting_kit:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Full Accounting Kit module not exist!'),
                }
            }

    @api.onchange('module_dynamic_accounts_report')
    def on_module_dynamic_accounts_report(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_dynamic_accounts_report'.replace("module_", ''))])
        if not modules and self.module_dynamic_accounts_report:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Dynamic Financial Reports BrainPack module not exist!'),
                }
            }

    @api.onchange('module_base_account_budget')
    def on_module_base_account_budget(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_base_account_budget'.replace("module_", ''))])
        if not modules and self.module_base_account_budget:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Budget Management module not exist!'),
                }
            }

    @api.onchange('module_brainpack_discuss_search_view_cr')
    def on_module_brainpack_discuss_search_view_cr(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_discuss_search_view_cr'.replace("module_", ''))])
        if not modules and self.module_brainpack_discuss_search_view_cr:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Search View On Discuss App module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp')
    def on_module_brainpack_meta_whatsapp(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Meta WhatsApp Graph API module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_discuss')
    def on_module_brainpack_meta_whatsapp_discuss(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_discuss'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_discuss:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Meta Whatsapp Discuss module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_marketing')
    def on_module_brainpack_meta_whatsapp_marketing(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_meta_whatsapp_marketing'.replace("module_", ''))])
        if not modules and self.module_brainpack_meta_whatsapp_marketing:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Meta Whatsapp Marketing module not exist!'),
                }
            }

    @api.onchange('module_brainpack_meta_whatsapp_chatbot')
    def on_module_brainpack_meta_whatsapp_chatbot(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brain_pack_backend_ent'.replace("module_", ''))])
        if not modules and self.module_brain_pack_backend_ent:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Meta Whatsapp ChatBot module not exist!'),
                }
            }

    @api.onchange('module_brain_pack_backend_ent')
    def on_module_brain_pack_backend_ent(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brain_pack_backend_ent'.replace("module_", ''))])
        if not modules and self.module_brain_pack_backend_ent:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Backend Enterprise Theme module not exist!'),
                }
            }

    @api.onchange('module_brainpack_debranding')
    def on_module_brainpack_debranding(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_debranding'.replace("module_", ''))])
        if not modules and self.module_brainpack_debranding:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Base module not exist!'),
                }
            }

    @api.onchange('module_brainpack_logo_on_login')
    def on_module_brainpack_logo_on_login(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_logo_on_login'.replace("module_", ''))])
        if not modules and self.module_brainpack_logo_on_login:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Logo on Login module not exist!'),
                }
            }

    @api.onchange('module_brainpack_mass_mailing_extended')
    def on_module_brainpack_mass_mailing_extended(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_mass_mailing_extended'.replace("module_", ''))])
        if not modules and self.module_brainpack_mass_mailing_extended:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Mass Mailing Extended module not exist!'),
                }
            }

    @api.onchange('module_brainpack_invoice_sale_portal_sign')
    def on_module_brainpack_invoice_sale_portal_sign(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_invoice_sale_portal_sign'.replace("module_", ''))])
        if not modules and self.module_brainpack_invoice_sale_portal_sign:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack Sale Invoice Portal Sign module not exist!'),
                }
            }

    @api.onchange('module_brainpack_im_livechat')
    def on_module_brainpack_im_livechat(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_im_livechat'.replace("module_", ''))])
        if not modules and self.module_brainpack_im_livechat:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Live Chat module not exist!'),
                }
            }

    @api.onchange('module_brain_mail_multicompany')
    def on_module_brain_mail_multicompany(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brain_mail_multicompany'.replace("module_", ''))])
        if not modules and self.module_brain_mail_multicompany:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Email Gateway Multi company module not exist!'),
                }
            }

    @api.onchange('module_project_timesheet_time_control')
    def on_module_mail_tracking(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_project_timesheet_time_control'.replace("module_", ''))])
        if not modules and self.module_project_timesheet_time_control:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Brainpack project timesheet time control module not exist!'),
                }
            }

    @api.onchange('module_mail_tracking')
    def on_module_mail_tracking(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_mail_tracking'.replace("module_", ''))])
        if not modules and self.module_mail_tracking:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Mail Tracking module not exist!'),
                }
            }

    @api.onchange('module_helpdesk_mgmt')
    def on_module_helpdesk_mgmt(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_helpdesk_mgmt'.replace("module_", ''))])
        if not modules and self.module_helpdesk_mgmt:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Helpdesk Management module not exist!'),
                }
            }

    @api.onchange('module_website_helpdesk_mgmt')
    def on_module_website_helpdesk_mgmt(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_website_helpdesk_mgmt'.replace("module_", ''))])
        if not modules and self.module_website_helpdesk_mgmt:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Website Helpdesk Mgmt module not exist!'),
                }
            }

    @api.onchange('module_brainpack_db_expiration')
    def on_module_brainpack_whatsapp_package(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_db_expiration'.replace("module_", ''))])
        if not modules and self.module_brainpack_db_expiration:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack DB Expiration module not exist!'),
                }
            }

    @api.onchange('module_brainpack_hr_access_rights')
    def on_module_brainpack_hr_access_rights(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_hr_access_rights'.replace("module_", ''))])
        if not modules and self.module_brainpack_hr_access_rights:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Hr Access Rights module not exist!'),
                }
            }

    @api.onchange('module_brainpack_hr_expense_extended')
    def on_module_brainpack_hr_expense_extended(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_hr_expense_extended'.replace("module_", ''))])
        if not modules and self.module_brainpack_hr_expense_extended:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('Braipack Hr Expense module not exist!'),
                }
            }

    @api.onchange('module_brainpack_website_extended')
    def on_module_brainpack_website_extended(self):
        ModuleSudo = self.env['ir.module.module'].sudo()
        modules = ModuleSudo.search(
            [('name', '=', 'module_brainpack_website_extended'.replace("module_", ''))])
        if not modules and self.module_brainpack_website_extended:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('BrainPack Website Extended module not exist!'),
                }
            }


