import ast
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_webservice(self):
        res = self.env['webservice.account'].sudo().search([], limit=1)
        return res.id

    def open_webservice_conf(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Webservice Configuration',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'webservice.account',
            'res_id': self.webservice_id.id,
            'target': 'current',
        }

    webservice_id = fields.Many2one('webservice.account', string="Webservice Config",default=_default_webservice, ondelete='cascade')
