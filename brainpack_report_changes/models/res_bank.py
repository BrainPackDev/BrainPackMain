from odoo import api, http, fields, models, tools

class ResBank(models.Model):
    _inherit = 'res.bank'

    iban_number = fields.Char("IBAN Number")

