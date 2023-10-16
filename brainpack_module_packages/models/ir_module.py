from odoo import api, http, fields, models, tools, modules
from odoo.addons.base.models.ir_module import assert_log_admin_access
from odoo.addons.base.models.ir_module import Module
from odoo.tools.parse_version import parse_version
import base64
from collections import defaultdict, OrderedDict
from decorator import decorator
from operator import attrgetter
import importlib
import io
import logging
import os
import pkg_resources
import shutil
import tempfile
import threading
import zipfile

import requests
import werkzeug.urls

from docutils import nodes
from docutils.core import publish_string
from docutils.transforms import Transform, writer_aux
from docutils.writers.html4css1 import Writer
import lxml.html
import psycopg2

import odoo
from odoo import api, fields, models, modules, tools, _
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG
from odoo.exceptions import AccessDenied, UserError
from odoo.osv import expression
from odoo.tools.parse_version import parse_version
from odoo.tools.misc import topological_sort
from odoo.tools.translate import TranslationImporter
from odoo.http import request
from odoo.modules import get_module_path, get_module_resource

_logger = logging.getLogger(__name__)

ACTION_DICT = {
    'view_mode': 'form',
    'res_model': 'base.module.upgrade',
    'target': 'new',
    'type': 'ir.actions.act_window',
}

class ModuleInherit(models.Model):
    _inherit = "ir.module.module"

    @assert_log_admin_access
    def button_uninstall(self):
        un_installable_modules = set(odoo.conf.server_wide_modules) & set(self.mapped('name'))
        if un_installable_modules:
            raise UserError(_("Those modules cannot be uninstalled: %s", ', '.join(un_installable_modules)))
        if any(state not in ('installed', 'to upgrade') for state in self.mapped('state')) and 'package' not in self.env.context:
            raise UserError(_(
                "One or more of the selected modules have already been uninstalled, if you "
                "believe this to be an error, you may try again later or contact support."
            ))
        deps = self.downstream_dependencies()
        (self + deps).write({'state': 'to remove'})
        return dict(ACTION_DICT, name=_('Uninstall'))