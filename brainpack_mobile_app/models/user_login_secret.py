import ast
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.Model):
    _name = 'user.login.secret'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users',string='User Id')
    access_token = fields.Char(string='Access Token')
