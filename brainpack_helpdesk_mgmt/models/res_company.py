from odoo import api, http, fields, models, tools

class Company(models.Model):
    _inherit = 'res.company'

    team_name = fields.Char(string="Team Name", default="BrainPack")