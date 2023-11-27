# -*- coding: utf-8 -*-

from odoo.modules.module import get_resource_path
from odoo import api, http, fields, models, tools, _
from odoo.http import request
import base64

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    affinda_integration = fields.Boolean(
        string='Affinda Integration', related='company_id.affinda_integration', readonly=False,)
    affinda_subscription = fields.Boolean(
        string='Affinda Integration', related='company_id.affinda_subscription', readonly=False, )
    affinda_api_key = fields.Char(
        'Api Key', related='company_id.affinda_api_key', readonly=False)
    affinda_api_url = fields.Char('Api Url', related='company_id.affinda_api_url', readonly=False)
    expense_collection = fields.Many2one(related='company_id.expense_collection', readonly=False,)