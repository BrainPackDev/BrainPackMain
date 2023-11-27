from odoo import _, api, fields, models, modules, tools
import requests
from odoo.exceptions import UserError
import json

class AffindaWorkspace(models.Model):
    _description = 'Affinda Workspace'
    _name = 'affinda.workspace'

    affinda_organization = fields.Many2one('affinda.organization','Affinda Organization')
    name = fields.Char('Name')
    identifier = fields.Char('Identifier')
    visibility = fields.Selection([
        ('organization', 'Organization'),
        ('private', 'Private'),
    ], default='organization')
    rejectInvalidDocuments = fields.Boolean("Reject Invalid Documents")
    rejectDuplicates = fields.Boolean('Reject Duplicates')
    documentSplitter = fields.Selection([
        ('leave', 'leave'),
        ('conservative', 'conservative'),
        ('recommended', 'recommended'),
        ('aggressive', 'aggressive'),
    ])
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    collection_ids = fields.One2many('affinda.workspace.collection', 'affinda_workspace', string='Collection(s)')
    count_collections = fields.Integer('Collection Count', compute='get_count_collections')

    def action_show_collection(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("brainpack_affinda_integration.affinda_workspace_collection_action")
        action['domain'] = [('id', 'in', self.collection_ids.ids)]
        action['context'] = {}
        return action

    @api.depends('collection_ids')
    def get_count_collections(self):
        for rec in self:
            count_collections = 0
            if rec.collection_ids:
                count_collections = len(rec.collection_ids)
            rec.count_collections = count_collections

    def action_create_workspace(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key:
                url = self.company_id.affinda_api_url + "/workspaces"

                payload = {
                    'organization': self.affinda_organization.identifier,
                    'name':self.name,
                }
                if self.visibility:
                    payload.update({'visibility':self.visibility})
                if self.rejectInvalidDocuments:
                    payload.update({'rejectInvalidDocuments':self.rejectInvalidDocuments})
                if self.rejectDuplicates:
                    payload.update({'rejectDuplicates':self.rejectDuplicates})
                if self.documentSplitter:
                    payload.update({'documentSplitter':self.documentSplitter})

                headers = {
                    "Authorization": "Bearer " + self.company_id.affinda_api_key,
                    "Content-Type": "application/json",
                }
                try:
                    response = requests.request("POST", url, headers=headers, json=payload)
                except requests.exceptions.ConnectionError:
                    raise UserError(
                        ("please check your internet connection."))
                if response.status_code == 201:
                    dict = json.loads(response.text)
                    self.write({
                        'identifier': dict.get('identifier'),
                    })

                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))
        else:
            raise UserError(
                ("Please check Your credentails!."))

    def action_delete_workspace(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key and self.identifier:
                url = self.company_id.affinda_api_url + "/workspaces/" + self.identifier
                headers = {
                    "Authorization": "Bearer " + self.company_id.affinda_api_key,
                    "Content-Type": "application/json",
                }
                try:
                    response = requests.delete(url, headers=headers)
                except requests.exceptions.ConnectionError:
                    raise UserError(
                        ("please check your internet connection."))
                if response.status_code == 204:
                    self.write({
                        'identifier': False,
                        'visibility': False,
                        'rejectInvalidDocuments': False,
                        'rejectDuplicates': False,
                        'documentSplitter': False,
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))
        else:
            raise UserError(
                ("Please check Your credentails!."))