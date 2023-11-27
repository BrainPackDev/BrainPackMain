from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from odoo.exceptions import ValidationError
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_payment_state(self):
        super()._compute_payment_state()
        for rec in self:
            if rec.payment_state == 'paid':
                orders = self.env['sale.order'].sudo().search([('invoice_ids', 'in', rec.ids),('is_subscription','=',True)])
                document_upload_product = orders.mapped('order_line').filtered(lambda x:x.product_id.id == self.env.ref('brainpack_affinda_subscription.product_affinda_doc_request').id)
                if document_upload_product:
                    document_upload_request = sum(document_upload_product.mapped('product_uom_qty'))
                    for order in orders:
                        try:
                            url = order.url
                            db = order.db_name
                            username = order.username
                            password = order.password

                            common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                            models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                            uid = common.login(db, username, password)

                            document_upload_requests = models.execute_kw(db, uid, password, 'ir.config_parameter',
                                                                 'search_read',
                                                                 [[['key', '=', 'brainpack_affinda_subscription.document_upload_requests']]],
                                                                 {'fields': ['value']})
                            if not document_upload_requests:
                                models.execute_kw(db, uid, password, 'ir.config_parameter', 'create', [
                                    {'value': str(document_upload_request),
                                     'key': 'brainpack_affinda_subscription.document_upload_requests'}])
                            else:
                                document_upload_request_rec = models.execute_kw(db, uid, password, 'ir.config_parameter',
                                                                           'search',
                                                                           [[['key', '=', 'brainpack_affinda_subscription.document_upload_requests']]])

                                document_upload_request = document_upload_request + float(document_upload_requests[0].get('value'))

                                if document_upload_request_rec:
                                    models.execute_kw(db, uid, password, 'ir.config_parameter',
                                                      'write',
                                                      [document_upload_request_rec,
                                                       {'value': str(document_upload_request)}])

                            company_rec = models.execute_kw(db, uid, password, 'res.company',
                                                                            'search',
                                                                            [[]])
                            if document_upload_request:
                                models.execute_kw(db, uid, password, 'res.company',
                                                  'write',
                                                  [company_rec,
                                                   {'affinda_subscription': True}])
                            else:
                                models.execute_kw(db, uid, password, 'res.company',
                                                  'write',
                                                  [company_rec,
                                                   {'affinda_subscription': False}])


                        except Exception as e:
                            # Show error popup if any exception occurs
                            _logger.error(e)
                            raise ValidationError(_("Error accessing db"))