from odoo import fields, models, api

whatsapp_package = ['brainpack_meta_whatsapp_chatbot','brainpack_meta_whatsapp_marketing','brainpack_meta_whatsapp_discuss','brainpack_meta_whatsapp']
accounting_package = ['base_account_budget','base_accounting_kit','dynamic_accounts_report']
brainpack_base_package = [
    'brainpack_db_expiration',
    'brainpack_hr_access_rights',
    'brainpack_hr_expense_extended',
    'brainpack_website_extended',
    'website_helpdesk_mgmt',
    'helpdesk_mgmt',
    'mail_tracking',
    'project_timesheet_time_control',
    'brain_mail_multicompany',
    'brainpack_im_livechat',
    'brainpack_invoice_sale_portal_sign',
    'brainpack_logo_on_login',
    'brainpack_mass_mailing_extended',
    'brainpack_debranding',
    'brain_pack_backend_ent',
    'sale_management',
    'account',
    'mass_mailing'
]
subacription_package = ['sale_subscription','sale_temporal','web_cohort']

class BrainpackModulePackage(models.Model):
    _name = 'brainpack.package'
    _description = 'BrainPack Module Package'

    name = fields.Char('Name')

    accounting_package = fields.Boolean('Accounting Package')
    whatsapp_package = fields.Boolean('Whatsapp Package')
    brainpack_base_package = fields.Boolean('BrainPack Base Package')
    subacription_package = fields.Boolean('Sale Subscription Package')


    def write(self, vals):
        res = super().write(vals)
        to_install = []
        to_uninstall = []

        if self.brainpack_base_package:
            to_install = to_install + brainpack_base_package
        else:
            to_uninstall = to_uninstall + brainpack_base_package

        if self.whatsapp_package:
            to_install = to_install + whatsapp_package
        else:
            to_uninstall = to_uninstall + whatsapp_package

        if self.accounting_package:
            to_install = to_install + accounting_package
        else:
            to_uninstall = to_uninstall + accounting_package

        if self.subacription_package:
            to_install = to_install + subacription_package
        else:
            to_uninstall = to_uninstall + subacription_package

        if to_install:
            moduless = self.env['ir.module.module'].search([('name','in',to_install)])
            for module in moduless:
                module.button_immediate_install()
        if to_uninstall:
            moduless = self.env['ir.module.module'].search([('name','in',to_uninstall)])
            for module in moduless:
                module.with_context(package=True).button_immediate_uninstall()
        return res

