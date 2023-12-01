from odoo import models, api
from odoo.http import request

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @api.model
    def get_frontend_session_info(self):
        result = super(IrHttp, self).get_frontend_session_info()
        result['in_quot_sign_add_field'] = self.env.company and self.env.company.in_quot_sign_add_field
        return result

