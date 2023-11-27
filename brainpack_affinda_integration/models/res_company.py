from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    affinda_integration = fields.Boolean('Affinda Integration',readonly=False)
    affinda_subscription = fields.Boolean('Affinda Subscription',readonly=False)
    affinda_api_url =  fields.Char('Api Url')
    affinda_api_key =  fields.Char('Api Key')
    expense_collection = fields.Many2one('affinda.workspace.collection','Collection')
