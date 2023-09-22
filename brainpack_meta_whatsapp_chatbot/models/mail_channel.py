from odoo import _, api, fields, models, modules, tools


class ChatbotMailChannel(models.Model):
    _inherit = 'mail.channel'

    wa_chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", string="Whatsapp Chatbot")
    message_ids = fields.One2many(
        'mail.message', 'res_id', domain=lambda self: [('wa_chatbot_id', '!=', False), ('wa_chatbot_id', '=', self.wa_chatbot_id.id)], string='Messages')
    script_sequence = fields.Integer(string='Sequence', default=1)
    is_chatbot_ended = fields.Boolean(string="Inactivate Chatbot")

class ChatbotMailMessage(models.Model):
    _inherit = 'mail.message'

    wa_chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", string="Whatsapp Chatbot")
