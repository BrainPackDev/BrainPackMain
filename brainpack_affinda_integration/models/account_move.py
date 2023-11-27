from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    affinda_move = fields.Boolean('Affinda Move')