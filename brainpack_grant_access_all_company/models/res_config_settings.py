import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    base_url = fields.Char('Base Url',related='company_id.base_url',readonly=False)
