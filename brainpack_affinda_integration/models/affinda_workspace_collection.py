from odoo import _, api, fields, models, modules, tools
import requests
from odoo.exceptions import UserError
import json

class AffindaWorkspaceCollection(models.Model):
    _description = 'Affinda Workspace Collection'
    _name = 'affinda.workspace.collection'

    affinda_workspace = fields.Many2one('affinda.workspace', 'Workspace')
    name = fields.Char('Name')
    identifier = fields.Char('Identifier')
    extractor = fields.Selection([
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('credit-note', 'Credit-note'),
    ])
    baseExtractor = fields.Char('Base Extractor')
    autoValidationThreshold = fields.Integer('Auto Validation Threshold')
    dateFormatPreference = fields.Selection([
        ('DMY', 'DMY'),
        ('MDY', 'MDY'),
        ('YMD', 'YMD'),
    ])
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    dateFormatFromDocument = fields.Char('Date Format From Document')
    allowOpenai = fields.Boolean('Allow Openai')
    trainsExtractor = fields.Boolean('Trains Extractor')

    def action_create_collection(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key:
                url = self.company_id.affinda_api_url + "/collections"

                payload = {
                    'workspace': self.affinda_workspace.identifier,
                    'name':self.name,
                }
                if self.extractor:
                    payload.update({'extractor':self.extractor})
                if self.baseExtractor:
                    payload.update({'baseExtractor':self.baseExtractor})
                if self.autoValidationThreshold:
                    payload.update({'autoValidationThreshold':self.autoValidationThreshold})
                if self.dateFormatPreference:
                    payload.update({'dateFormatPreference':self.dateFormatPreference})
                if self.autoValidationThreshold:
                    payload.update({'autoValidationThreshold':self.autoValidationThreshold})
                if self.dateFormatPreference:
                    payload.update({'dateFormatPreference':self.dateFormatPreference})
                if self.allowOpenai:
                    payload.update({'allowOpenai':self.allowOpenai})
                if self.trainsExtractor:
                    payload.update({'trainsExtractor':self.trainsExtractor})

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

    def action_delete_collection(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key and self.identifier:
                url = self.company_id.affinda_api_url + "/collections/" + self.identifier
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
                        'extractor': False,
                        'baseExtractor': False,
                        'autoValidationThreshold': False,
                        'dateFormatPreference': False,
                        'dateFormatFromDocument': False,
                        'allowOpenai': False,
                        'trainsExtractor': False,
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))