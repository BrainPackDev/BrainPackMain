from ast import literal_eval

from odoo import api, fields, models,_


class ResCompany(models.Model):
    _inherit = 'res.company'

    wa_chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", string="Whatsapp Chatbot")