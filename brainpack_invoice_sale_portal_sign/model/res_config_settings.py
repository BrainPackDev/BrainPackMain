from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    in_quot_sign_add_field = fields.Boolean(related='company_id.in_quot_sign_add_field',readonly=False)