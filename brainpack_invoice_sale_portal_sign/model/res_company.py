from odoo import api, fields, models, _

class Company(models.Model):
    _inherit = 'res.company'

    in_quot_sign_add_field = fields.Boolean('Quotation Sign Add Field')