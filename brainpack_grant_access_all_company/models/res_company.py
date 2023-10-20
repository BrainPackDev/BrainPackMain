from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    base_url = fields.Char('Base Url')