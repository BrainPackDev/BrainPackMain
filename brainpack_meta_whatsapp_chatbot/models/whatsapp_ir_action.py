from odoo import models, fields, api


class WhatsAppIrAction(models.Model):
    _name = 'whatsapp.ir.actions'

    name = fields.Char(string='Action Name', required=True, translate=True)
    binding_model_id = fields.Many2one('ir.model', ondelete='cascade')
    chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", string="Chatbot")