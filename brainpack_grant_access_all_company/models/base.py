# -*- coding: utf-8 -*-

from odoo import models
from odoo.models import BaseModel

class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def get_base_url(self):
        if len(self) > 1:
            raise ValueError("Expected singleton or no record: %s" % self)
        if self.env.company and self.env.company.base_url:
            return self.env.company.base_url
        else:
            return self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    BaseModel.get_base_url = get_base_url