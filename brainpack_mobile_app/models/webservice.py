# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
import string
import random
import base64

def _default_unique_key(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))



class WebServiceAccount(models.Model):
	_name = 'webservice.account'
	_description = "Web Service Acccount"


	name = fields.Char(
		string="Name",
		required = True
	)
	key  = fields.Char(
		string="Key"
		# required = True

	)
	hash_val = fields.Char(string="Hash Val")
	algo = fields.Selection(
		string = 'Authorization Algo',
		selection = [('base64', 'Base64')],
		default = 'base64',
		required = True
	)
	state = fields.Selection(
		string = 'State',
		selection = [('base64', 'Base64')],
		default = 'base64'
	)
	key_state = fields.Selection(
		[('draft', 'Draft'),('confirm',"Confirm")],
		default = 'draft'
	)

	def set_to_draft(self):
		self.key_state = "draft"

	def set_to_confirm(self):
		for o in self:
			if o.key:
				o.key_state = "confirm"
			else:
				raise UserError("Click on 'Generate Api Secret Key' to confirm this service account")

	def generate_secret_key(self):
		self.key = _default_unique_key(18)
		self.hash_val = base64.b64encode(self.key.encode())
		print(">>>>>>>>>>>", self.key)


	
	def copy(self, default=None):
		raise UserError(_("You can't duplicate this Configuration."))

	def get_hash(self):
		self.ensure_one()
		return base64.b64encode(self.key.encode())
