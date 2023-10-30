from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from odoo.http import request

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    utm_source = fields.Char('UTM source',tracking=True)
    utm_campaign = fields.Char('UTM Campaign',tracking=True)
    utm_medium = fields.Char('UTM Medium',tracking=True)
    utm_term = fields.Char('UTM Term',tracking=True)
    utm_content = fields.Char('UTM Content',tracking=True)
    utm_id = fields.Char('UTM Campaign ID',tracking=True)
    website_url = fields.Char('Website URL',tracking=True)