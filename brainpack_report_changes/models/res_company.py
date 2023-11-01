from odoo import api, http, fields, models, tools

class Company(models.Model):
    _inherit = 'res.company'

    brain_pack_report_font_color = fields.Char('Report Font Color', default='#137EE8')
    general_comopany_name = fields.Char('General Name', default='BrainPack')