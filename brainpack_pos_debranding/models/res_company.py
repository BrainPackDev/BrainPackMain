from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
class ResCompany(models.Model):
    _inherit = 'res.company'

    pos_logo = fields.Binary('POS logo',store=True)