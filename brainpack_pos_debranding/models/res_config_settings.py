import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_logo = fields.Binary(related='company_id.pos_logo', string="POS Logo",readonly=False)
