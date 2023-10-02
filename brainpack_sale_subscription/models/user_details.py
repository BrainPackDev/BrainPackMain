from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from xmlrpc import client as xmlrpclib
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class UserDetails(models.Model):
    _name = 'user.details'

    user_id = fields.Integer('User Id', tracking=True)
    user_name = fields.Char('User Name', tracking=True)
    create_time = fields.Datetime('Create Time', tracking=True)
    active_user = fields.Boolean('Active User', tracking=True)
    user_exits = fields.Selection([
		('exits', 'Exists'),
		('not_exits', 'Not Exists'),
	], string="Record Exits/Not Exits")
    subscription_id = fields.Many2one('sale.order')
    active_day = fields.Integer("Active Day")

