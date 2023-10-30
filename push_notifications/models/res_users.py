# -*- coding: utf-8 -*-
import datetime
from odoo import _, api, fields, models
from odoo.exceptions import UserError

# pip3 install pyfcm
class ResUsers(models.Model):
    _inherit = 'res.users'

    device_type = fields.Char(string="Device Type")
    unique_id = fields.Char(string="Unique ID")
    mo_app_version = fields.Float(string="Mobile App Version")
    fcm_token = fields.Char(string="FCM Token", help="Firebase cloud messaging")
    
    