from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def onchange_ks_next_invoice_date(self):
        for rec in self:
            if rec.url and rec.db_name and rec.username and rec.password:
                try:
                    url = rec.url
                    db = rec.db_name
                    username = rec.username
                    password = rec.password

                    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                    uid = common.login(db, username, password)
                    db_expiration_date = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                           [[['key', '=', 'database.expiration_date']]],
                                                           {'fields': ['value']})

                    if not db_expiration_date:
                        models.execute_kw(db, uid, password, 'ir.config_parameter', 'create' ,
                            [{'value' :rec.next_invoice_date.strftime("%Y-%m-%d %H:%M:%S")
                             ,'key' :'database.expiration_date'}])
                    else:
                        db_expiration_date_rec = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search',
                                                                   [[['key', '=', 'database.expiration_date']]])

                        if db_expiration_date_rec:
                            models.execute_kw(db, uid, password, 'ir.config_parameter',
                                              'write',
                                              [db_expiration_date_rec, {'value' :rec.next_invoice_date.strftime("%Y-%m-%d %H:%M:%S")}])

                    rec.db_expiration_date = rec.next_invoice_date

                    for user_detail in rec.user_details_ids:
                        user_detail.write({'active_day' :0})
                except Exception as e:
                    # Show error popup if any exception occurs
                    _logger.error(e)
                    raise ValidationError(_("Error accessing db"))