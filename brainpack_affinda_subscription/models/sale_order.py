from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_uploaded_requests = fields.Float('Uploaded Requests')
    remaining_uploaded_requests = fields.Float('Remaining Uploaded Requests')

    def update_document_requests(self):
        for rec in self.sudo().search([('is_subscription', '=', True)]):
            if rec.url and rec.db_name and rec.username and rec.password:
                url = rec.url
                db = rec.db_name
                username = rec.username
                password = rec.password

                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                uid = common.login(db, username, password)

                organizations = models.execute_kw(db, uid, password, 'affinda.organization', 'search_read',
                                          [[]],
                                          {'fields': ['id', 'uploaded_doc_count']})
                total_uploaded_requests = 0
                for org in organizations:
                    total_uploaded_requests = total_uploaded_requests + org.get('uploaded_doc_count')

                rec.write({'total_uploaded_requests': total_uploaded_requests})

                document_upload_requests = models.execute_kw(db, uid, password, 'ir.config_parameter',
                                                             'search_read',
                                                             [[['key', '=',
                                                                'brainpack_affinda_subscription.document_upload_requests']]],
                                                             {'fields': ['value']})

                if document_upload_requests:
                    rec.write({'remaining_uploaded_requests': float(document_upload_requests[0].get('value'))})
