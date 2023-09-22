from ast import literal_eval

from odoo import api, fields, models,_


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wa_chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", related='company_id.wa_chatbot_id',string="Whatsapp Chatbot",readonly=False)