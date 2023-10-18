# -*- coding: utf-8 -*-

from odoo import api, Command, fields, models, _, _lt
from odoo.osv import expression

class AccountAnalyticLineInherit(models.Model):
    _inherit = 'account.analytic.line'

    def _timesheet_get_portal_domain(self):
        domain = super(AccountAnalyticLineInherit, self)._timesheet_get_portal_domain()
        if 'website_id' in self.env.context and self.env.context.get('website_id'):
            website = self.env['website'].sudo().browse(self.env.context.get('website_id'))
            domain += [('company_id', '=', website.company_id.id)]
        return expression.AND([domain, []])