from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _
from odoo.exceptions import UserError, ValidationError
import ast

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    documents = fields.Many2many('affinda.document',stirng="Document(s)")

    def total_amount_update(self):
        self.ensure_one()
        if self.documents:
            expense_total = 0
            currency_id = False
            for doc in self.documents:
                if doc.document_response:
                    res_dict = ast.literal_eval(doc.document_response)
                    if 'paymentAmountTotal' in res_dict and res_dict.get('paymentAmountTotal'):
                        if res_dict.get('paymentAmountTotal').get('parsed'):
                            expense_total = expense_total + float(res_dict.get('paymentAmountTotal').get('parsed'))
                    if 'currencyCode' in res_dict and res_dict.get('currencyCode'):
                        currency_id = self.env['res.currency'].sudo().search(
                            [('name', '=', res_dict.get('currencyCode').get('parsed').get('value'))])


            self.write({'total_amount': expense_total,'currency_id':currency_id.id if currency_id else self.company_id.currency_id.id})

    def affinda_doc_create(self, attachments, affinda_workspace_collection):
        self.ensure_one()
        for attachment in attachments:
            affinda_doc = self.env['affinda.document'].sudo().search([('attachment_id', '=', attachment.id)])

            if not affinda_doc:
                document = self.env['affinda.document'].sudo().create({
                    'affinda_workspace_collection': affinda_workspace_collection.id,
                    'affinda_workspace': affinda_workspace_collection.affinda_workspace.id if affinda_workspace_collection.affinda_workspace else False,
                    'extractor': affinda_workspace_collection.extractor if affinda_workspace_collection.extractor else False,
                    'attachment_id': attachment.id,
                    'file': attachment.datas,
                    'file_name': attachment.name,
                })
                document.action_create_document()
                self.write({'documents': [(4, document.id)]})


    def get_total_from_documents(self):
        affinda_workspace_collection = False

        if self.company_id and self.company_id.expense_collection:
            affinda_workspace_collection = self.company_id.expense_collection
        else:
            affinda_workspace_collection = self.env.company.expense_collection

        if affinda_workspace_collection:
            attachments = self.env['ir.attachment'].sudo().search([('res_id', '=', self.id),('res_model','=','hr.expense')])
            self.affinda_doc_create(attachments,affinda_workspace_collection)
            self.total_amount_update()
        else:
            raise UserError(_("Collection configuration missing. Please contact administrator."))

    def attach_document(self, **kwargs):
        affinda_workspace_collection = False

        if self.company_id and self.company_id.expense_collection:
            affinda_workspace_collection = self.company_id.expense_collection
        else:
            affinda_workspace_collection = self.env.company.expense_collection

        if affinda_workspace_collection:

            if 'attachment_ids' in kwargs:
                attachments = self.env['ir.attachment'].sudo().search([('id','in',kwargs.get('attachment_ids'))])
                self.affinda_doc_create(attachments, affinda_workspace_collection)

            self.total_amount_update()

        else:
            raise UserError(_("Collection configuration missing. Please contact administrator."))
