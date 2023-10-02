from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    url = fields.Char("Server URL")
    db_name = fields.Char("DB Name")
    username = fields.Char("Username")
    password = fields.Char("Password")
    creation_date_db = fields.Datetime("DB Creation Date")
    db_expiration_date = fields.Datetime(string="DB Expiration Date")
    db_expiration_reason = fields.Text("DB Expiration Reason")
    user_details_ids = fields.One2many("user.details","subscription_id",string="User Details")
    # db_enterprise_code = fields.Text("DB Enterprise Code")

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
                        models.execute_kw(db, uid, password, 'ir.config_parameter', 'create',[{'value':rec.next_invoice_date.strftime("%Y-%m-%d %H:%M:%S"),'key':'database.expiration_date'}])
                    else:
                        db_expiration_date_rec = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search',
                                         [[['key', '=', 'database.expiration_date']]])

                        if db_expiration_date_rec:
                            models.execute_kw(db, uid, password, 'ir.config_parameter',
                                                                   'write',
                                                                   [db_expiration_date_rec, {'value':rec.next_invoice_date.strftime("%Y-%m-%d %H:%M:%S")}])

                    rec.db_expiration_date = rec.next_invoice_date

                    for user_detail in rec.user_details_ids:
                        user_detail.write({'active_day':0})
                except Exception as e:
                    # Show error popup if any exception occurs
                    _logger.error(e)
                    raise ValidationError(_("Error accessing db"))


    def get_config_parameters(self):
        # Method to fetch database creation,expiry data from system parameters This method will be called when clicked on "GET DB PARAMETERS" button shown on header of brainpack.sale.subscription model form view.
        for rec in self:
            db_creation_date = False
            db_expiration_date = False
            db_expiration_reason = False
            # db_enterprise_code = False
            if rec.url and rec.db_name and rec.username and rec.password:
                try:
                    url = rec.url
                    db = rec.db_name
                    username = rec.username
                    password = rec.password

                    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                    uid = common.login(db, username, password)

                    db_creation_date = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                         [[['key', '=', 'database.create_date']]],
                                                         {'fields': ['value']})
                    db_expiration_date = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                           [[['key', '=', 'database.expiration_date']]],
                                                           {'fields': ['value']})
                    db_expiration_reason = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                                                             [[['key', '=', 'database.expiration_reason']]],
                                                             {'fields': ['value']})
                    # db_enterprise_code = models.execute_kw(db, uid, password, 'ir.config_parameter', 'search_read',
                    #                                        [[['key', '=', 'database.enterprise_code']]],
                    #                                        {'fields': ['value']})

                except Exception as e:
                    # Show error popup if any exception occurs
                    _logger.error(e)
                    raise ValidationError(_("Error accessing db"))

                # Update the record with newly fetched data
                rec.write({
                    'creation_date_db': datetime.strptime(db_creation_date[0].get('value'),
                                                          '%Y-%m-%d %H:%M:%S') if db_creation_date and db_creation_date[
                        0].get('value') else False,
                    'db_expiration_date': datetime.strptime(db_expiration_date[0].get('value'),
                                                            '%Y-%m-%d %H:%M:%S') if db_expiration_date and
                                                                                    db_expiration_date[0].get(
                                                                                        'value') else False,
                    'db_expiration_reason': db_expiration_reason and db_expiration_reason[0].get('value') or False,
                    # 'db_enterprise_code': db_enterprise_code and db_enterprise_code[0].get('value') or False,
                })


                _logger.info('record with id: %s updated successfully' % rec.id)
            else:
                raise UserError(_('Server URL, DB Name, Username and Password are required for Get DB Parameters.'))


    def get_user_details(self):
        for rec in self.sudo().search([('is_subscription','=',True)]):
            if rec.url and rec.db_name and rec.username and rec.password:
                url = rec.url
                db = rec.db_name
                username = rec.username
                password = rec.password

                common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
                models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)
                uid = common.login(db, username, password)

                users = models.execute_kw(db, uid, password, 'res.users', 'search_read', [[['id','not in',[1,2,3,4,5,6,7]],['active','in',[True, False]]]], {'fields': ['id','name','create_date','active','password','groups_id']})

                for user in users:
                    has_group = models.execute_kw(db,uid, password, 'ir.model.data', 'check_object_reference',['base','group_user'])
                    if has_group and has_group[1] in user.get('groups_id'):
                        group_users = models.execute_kw(db,uid, password, 'res.groups', 'search_read',[[['id','=',has_group[1]]]], {'fields': ['users']})
                        if user.get('id') in rec.user_details_ids.mapped('user_id'):
                            user_detail = rec.user_details_ids.filtered(lambda x:x.user_id == user.get('id'))
                            user_detail.sudo().write({
                                'user_id': user.get('id'),
                                'user_name': user.get('name'),
                                'create_time': user.get('create_date'),
                                'active_user': user.get('active'),
                                'user_exits': 'exits',
                                'active_day':user_detail.active_day + 1 if user.get('active') else 0,
                            })
                        else:
                            self.env['user.details'].sudo().create({
                                'user_id':user.get('id'),
                                'user_name':user.get('name'),
                                'create_time':user.get('create_date'),
                                'active_user':user.get('active'),
                                'subscription_id':rec.id,
                                'user_exits': 'exits',
                                'active_day': 1 if user.get('active') else 0,
                            })

                usr_lst = [usr.get('id') for usr in users]

                for user_detail in rec.user_details_ids:
                    if user_detail.user_id not in usr_lst:
                        user_detail.write({'user_exits':'not_exits'})



