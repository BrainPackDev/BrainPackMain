from odoo import _, api, fields, models, modules, tools
import requests
from odoo.exceptions import UserError
import json
import ast
import re
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class AffindaDocument(models.Model):
    _description = 'Affinda Document'
    _name = 'affinda.document'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'file_name'
    _order = 'write_date desc, create_date desc'

    affinda_workspace = fields.Many2one('affinda.workspace', 'Workspace')
    affinda_workspace_collection = fields.Many2one('affinda.workspace.collection', 'collection')
    extractor = fields.Selection([
        ('invoice', 'Invoice'),
        ('receipt', 'Receipt'),
        ('credit-note', 'Credit-note'),
    ],related='affinda_workspace_collection.extractor')
    file = fields.Binary()
    file_name = fields.Char(string="File Name")
    attachment_id = fields.Many2one('ir.attachment',string="Attachment")
    identifier = fields.Char('Identifier')
    document_response = fields.Text('Document Response')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    move_id = fields.Many2one('account.move',string='Move')
    move_count = fields.Integer('Move Count', compute='get_move_count')

    @api.depends('move_id')
    def get_move_count(self):
        for rec in self:
            move_count = 0
            if rec.move_id:
                move = self.env['account.move'].search([('id', '=', rec.move_id.id)])
                move_count = len(move)
            rec.move_count = move_count

    def open_credit_move(self):
        credits = self.mapped('move_id')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_refund_type')
        if len(credits) > 1:
            action['domain'] = [('id', 'in', credits.ids)]
        elif len(credits) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = credits.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_refund',
        }
        action['context'] = context
        return action

    def open_receipt_move(self):
        receipts = self.mapped('move_id')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_receipt_type')
        if len(receipts) > 1:
            action['domain'] = [('id', 'in', receipts.ids)]
        elif len(receipts) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = receipts.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_receipt',
        }
        action['context'] = context
        return action

    def open_invoice_move(self):
        invoices = self.mapped('move_id')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action



    @api.model
    def create(self, vals):
        res = super(AffindaDocument, self).create(vals)
        for rec in res:
            attachment = self.env['ir.attachment'].sudo().create({
                 'name': rec.file_name,
                'datas': rec.file,
                'type': 'binary',
                'res_model':'affinda.document',
                'res_id':rec.id,
            })
            if attachment:
                res.attachment_id = attachment.id
        return res

    def write(self, vals):
        res = super(AffindaDocument, self).write(vals)
        if 'file' in vals:
            attachment = self.env['ir.attachment'].sudo().create({
                'name': self.file_name,
                'datas': self.file,
                'type': 'binary',
                'res_model': 'affinda.document',
                'res_id': self.id,
            })
            if attachment:
                self.attachment_id = attachment.id
        return res

    def get_partner_move(self,res_dict):
        partner = False

        city = False
        street2 = ''
        zip = False
        state_id = False
        country_id = False
        street = False
        email = False
        phone = False
        vat = False

        invoice_partner_id = False

        delivery_city = False
        delivery_street2 = ''
        delivery_zip = False
        delivery_state_id = False
        delivery_country_id = False
        delivery_street = False

        delivery_partner_id = False

        if res_dict.get('customerVat'):
            if 'raw' in res_dict.get('customerVat') and res_dict.get('customerVat').get('raw'):
                vat = res_dict.get('customerVat').get('raw')

        if res_dict.get('customerEmail'):
            if 'raw' in res_dict.get('customerEmail') and res_dict.get('customerEmail').get('raw'):
                email = res_dict.get('customerEmail').get('raw')

        if res_dict.get('customerPhoneNumber'):
            if 'raw' in res_dict.get('customerPhoneNumber') and res_dict.get('customerPhoneNumber').get('raw'):
                phone = res_dict.get('customerPhoneNumber').get('raw')

        if res_dict.get('customerBillingAddress'):
            if 'parsed' in res_dict.get('customerBillingAddress'):
                location_dict = res_dict.get('customerBillingAddress').get('parsed')

            if location_dict.get('streetNumber'):
                street2 = str(street2) + location_dict.get('streetNumber') + ', '
            if location_dict.get('street'):
                street2 = str(street2) + location_dict.get('street') + ' '

            if location_dict.get('apartmentNumber'):
                street2 = str(street2) + location_dict.get('apartmentNumber') + ', '

            if location_dict.get('city'):
                city = location_dict.get('city')

            if location_dict.get('postalCode'):
                zip = location_dict.get('postalCode')

            if location_dict.get('state'):
                state = self.env['res.country.state'].sudo().search([('name', '=', location_dict.get('state'))], limit=1)
                if state:
                    state_id = state.id

            if location_dict.get('country'):
                country = self.env['res.country'].sudo().search([('name', '=', location_dict.get('country'))],
                                                              limit=1)
                if country:
                    country_id = country.id
            if location_dict.get('countryCode'):
                country = self.env['res.country'].sudo().search([('code', '=', location_dict.get('countryCode'))],
                                                              limit=1)
                if country:
                    country_id = country.id

            if 'raw' in res_dict.get('customerBillingAddress'):
                street = res_dict.get('customerBillingAddress').get('raw')

        if res_dict.get('customerDeliveryAddress'):
            if 'parsed' in res_dict.get('customerDeliveryAddress'):
                location_dict = res_dict.get('customerDeliveryAddress').get('parsed')

            if location_dict.get('streetNumber'):
                delivery_street2 = str(delivery_street2) + location_dict.get('streetNumber') + ', '
            if location_dict.get('street'):
                delivery_street2 = str(delivery_street2) + location_dict.get('street') + ' '

            if location_dict.get('apartmentNumber'):
                delivery_street2 = str(delivery_street2) + location_dict.get('apartmentNumber') + ', '

            if location_dict.get('city'):
                delivery_city = location_dict.get('city')

            if location_dict.get('postalCode'):
                delivery_zip = location_dict.get('postalCode')

            if location_dict.get('state'):
                state = self.env['res.country.state'].sudo().search([('name', '=', location_dict.get('state'))],
                                                                    limit=1)
                if state:
                    delivery_state_id = state.id

            if location_dict.get('country'):
                country = self.env['res.country'].sudo().search([('name', '=', location_dict.get('country'))],
                                                                limit=1)
                if country:
                    delivery_country_id = country.id
            if location_dict.get('countryCode'):
                country = self.env['res.country'].sudo().search([('code', '=', location_dict.get('countryCode'))],
                                                                limit=1)
                if country:
                    delivery_country_id = country.id

            if 'raw' in res_dict.get('customerDeliveryAddress'):
                delivery_street = res_dict.get('customerDeliveryAddress').get('raw')

        if res_dict.get('customerCompanyName') and not res_dict.get('customerContactName'):

            if res_dict.get('customerCompanyName') and res_dict.get('customerCompanyName').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('name', '=', res_dict.get('customerCompanyName').get('raw')), ('is_company', '=', True)], limit=1)
            if res_dict.get('customerVat') and res_dict.get('customerVat').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('vat', '=', res_dict.get('customerVat').get('raw')), ('is_company', '=', True)], limit=1)
            if res_dict.get('customerPhoneNumber') and res_dict.get('customerPhoneNumber').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('phone', '=', res_dict.get('customerPhoneNumber').get('raw')), ('is_company', '=', True)],
                  limit=1)
            if res_dict.get('customerEmail') and res_dict.get('customerEmail').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('email', '=', res_dict.get('customerEmail').get('raw')), ('is_company', '=', True)], limit=1)

            if not partner:
                partner_vals = {
                  'name': res_dict.get('customerCompanyName').get('raw'),
                  'city': city,
                  'street2': street2,
                  'zip': zip,
                  'state_id': state_id,
                  'country_id': country_id,
                  'street': street,
                  'email': email,
                  'phone': phone,
                  'vat': vat,
                  'is_company':True
                }

                partner = self.env['res.partner'].sudo().create(partner_vals)

        elif not res_dict.get('customerCompanyName') and res_dict.get('customerContactName'):

            if res_dict.get('customerContactName') and res_dict.get('customerContactName').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('name', '=', res_dict.get('customerContactName').get('raw')), ('is_company', '=', False)], limit=1)
            if res_dict.get('customerVat') and res_dict.get('customerVat').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('vat', '=', res_dict.get('customerVat').get('raw')), ('is_company', '=', False)], limit=1)
            if res_dict.get('customerPhoneNumber') and res_dict.get('customerPhoneNumber').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('phone', '=', res_dict.get('customerPhoneNumber').get('raw')), ('is_company', '=', False)],
                  limit=1)
            if res_dict.get('customerEmail') and res_dict.get('customerEmail').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('email', '=', res_dict.get('customerEmail').get('raw')), ('is_company', '=', False)], limit=1)

            if not partner:
                partner_vals = {
                  'name': res_dict.get('customerContactName').get('raw'),
                  'city': city,
                  'street2': street2,
                  'zip': zip,
                  'state_id': state_id,
                  'country_id': country_id,
                  'street': street,
                  'email': email,
                  'phone': phone,
                  'vat': vat,
                  'is_company': False
                }

                partner = self.env['res.partner'].sudo().create(partner_vals)
        elif res_dict.get('customerCompanyName') and res_dict.get('customerContactName'):
            if res_dict.get('customerContactName') and res_dict.get('customerContactName').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('name', '=', res_dict.get('customerContactName').get('raw')), ('is_company', '=', False)], limit=1)
            if res_dict.get('customerVat') and res_dict.get('customerVat').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('vat', '=', res_dict.get('customerVat').get('raw')), ('is_company', '=', False)], limit=1)
            if res_dict.get('customerPhoneNumber') and res_dict.get('customerPhoneNumber').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('phone', '=', res_dict.get('customerPhoneNumber').get('raw')), ('is_company', '=', False)],
                  limit=1)
            if res_dict.get('customerEmail') and res_dict.get('customerEmail').get('raw') != '':
                partner = self.env['res.partner'].sudo().search(
                  [('email', '=', res_dict.get('customerEmail').get('raw')), ('is_company', '=', False)], limit=1)

            if not partner:
                company_vals = {
                    'name' : res_dict.get('customerCompanyName').get('raw'),
                    'city': city,
                    'street2': street2,
                    'zip': zip,
                    'state_id': state_id,
                    'country_id': country_id,
                    'street': street,
                    'vat': vat,
                    'is_company': True
                }
                company = self.env['res.partner'].sudo().create(company_vals)
                partner_vals = {
                  'name': res_dict.get('customerContactName').get('raw'),
                  'city': city,
                  'street2': street2,
                  'zip': zip,
                  'state_id': state_id,
                  'country_id': country_id,
                  'street': street,
                  'email': email,
                  'phone': phone,
                  'vat': vat,
                  'parent_id': company.id,
                  'is_company': False
                }

                partner = self.env['res.partner'].sudo().create(partner_vals)

        if partner:
            invoice_partner_id = self.env['res.partner'].sudo().search([('type','=','invoice'),('parent_id','=',partner.id)],limit=1)

            if city or street2 or zip or state_id or country_id or street:
                invoice_vals = {
                    'city': city,
                    'street2': street2,
                    'zip': zip,
                    'state_id': state_id,
                    'country_id': country_id,
                    'street': street,
                    'type': 'invoice',
                }
                if invoice_partner_id:
                    invoice_partner_id.write(invoice_vals)
                else:
                    invoice_vals.update({
                        'parent_id' : partner.id,
                    })
                    self.env['res.partner'].sudo().create(invoice_vals)

            delivery_partner_id = self.env['res.partner'].sudo().search(
                [('type', '=', 'delivery'), ('parent_id', '=', partner.id)], limit=1)

            if delivery_city or delivery_street2 or delivery_zip or delivery_state_id or delivery_country_id or delivery_street:
                delivery_vals = {
                    'city': delivery_city,
                    'street2': delivery_street2,
                    'zip': delivery_zip,
                    'state_id': delivery_state_id,
                    'country_id': delivery_country_id,
                    'street': delivery_street,
                    'type': 'delivery',
                }

                if delivery_partner_id:
                    delivery_partner_id.write(delivery_vals)
                else:
                    delivery_vals.update({
                        'parent_id' : partner.id,
                    })
                    self.env['res.partner'].sudo().create(delivery_vals)

        return partner

    def parepare_move_line(self, res_dict):
        move_lines = []
        if res_dict.get('tablesBeta'):
            for tablesBetaData in res_dict.get('tablesBeta'):
                if 'parsed' in tablesBetaData and tablesBetaData.get('parsed'):
                    if 'rows' in tablesBetaData.get('parsed') and tablesBetaData.get('parsed').get('rows'):
                        for row in tablesBetaData.get('parsed').get('rows'):
                            if 'parsed' in row and row.get('parsed'):
                                parsed_dict = row.get('parsed')
                                if 'itemDescriptionBeta' in parsed_dict and parsed_dict.get('itemDescriptionBeta'):
                                    product_name = parsed_dict.get('itemDescriptionBeta').get('parsed')
                                    product = self.env['product.product'].sudo().search([('name','=',product_name)])
                                    product_uom = False
                                    product_price = 1
                                    itemQuantityBeta = 1

                                    if 'itemQuantityBeta' in parsed_dict and parsed_dict.get('itemQuantityBeta'):
                                        itemQuantityBeta = parsed_dict.get('itemQuantityBeta').get('parsed')

                                    if 'itemUnitBeta' in parsed_dict and parsed_dict.get('itemUnitBeta'):
                                        product_uom_id = self.env['uom.uom'].sudo().search([('name','=',parsed_dict.get('itemUnitBeta').get('parsed'))])
                                        if product_uom_id:
                                            product_uom = product_uom_id.id

                                    if 'itemUnitPriceBeta' in parsed_dict and parsed_dict.get('itemUnitPriceBeta'):
                                        product_price = float(parsed_dict.get('itemUnitPriceBeta').get('parsed'))

                                    if not product:
                                        product_vals = {
                                            'name' : product_name,
                                            'list_price' : product_price,
                                        }
                                        if product_uom:
                                            product_vals.update({
                                                'uom_id':product_uom,
                                            })
                                        product = self.env['product.product'].sudo().create(product_vals)

                                    tax_ids = []


                                    if 'itemTaxRateBeta' in parsed_dict and parsed_dict.get('itemTaxRateBeta'):
                                        tax = False
                                        if '%' in parsed_dict.get('itemTaxRateBeta').get('raw'):
                                            lst_tax = re.findall(r'\b\d+\b',
                                                                 parsed_dict.get('itemTaxRateBeta').get('parsed'))
                                            if lst_tax:
                                                tax_amount = lst_tax[0]
                                                # tax_amount = parsed_dict.get('itemTaxRateBeta').get('parsed').replace('%','')
                                                if tax_amount:
                                                    tax = self.env['account.tax'].sudo().search([('amount','=',float(tax_amount)),('type_tax_use','=','sale'),('amount_type','=','percent'),('company_id','=',self.company_id.id)])
                                                    if not tax:
                                                        tax = self.env['account.tax'].sudo().create({
                                                            'name' : 'Tax ' + parsed_dict.get('itemTaxRateBeta').get('raw'),
                                                            'amount_type' : 'percent',
                                                            'type_tax_use' : 'sale',
                                                            'amount' : float(tax_amount),
                                                            'company_id': self.company_id.id
                                                        })
                                        else:
                                            lst_tax = re.findall(r'\b\d+\b', parsed_dict.get('itemTaxRateBeta').get('raw'))
                                            if lst_tax:
                                                tax_amount = lst_tax[0]
                                                if tax_amount:
                                                    tax = self.env['account.tax'].sudo().search(
                                                        [('amount', '=', float(tax_amount)),
                                                         ('type_tax_use', '=', 'sale'),
                                                         ('amount_type', '=', 'fixed'),('company_id','=',self.company_id.id)])
                                                    if not tax:
                                                        tax = self.env['account.tax'].sudo().create({
                                                            'name': 'Tax ' + parsed_dict.get('itemTaxRateBeta').get(
                                                                'raw'),
                                                            'amount_type': 'fixed',
                                                            'type_tax_use': 'sale',
                                                            'amount': float(tax_amount),
                                                            'company_id': self.company_id.id
                                                        })
                                        if tax:
                                            tax_ids.append((4, tax.id))

                                    line_val = {
                                        'product_id': product.id,
                                        'price_unit': product_price,
                                        'product_uom_id': product_uom or product.uom_id.id,
                                        'tax_ids' : tax_ids,
                                        'quantity' : itemQuantityBeta,
                                    }

                                    move_lines.append(line_val)

        paymentAmountTax = False
        if 'paymentAmountTax' in res_dict and res_dict.get('paymentAmountTax'):
            if '%' in res_dict.get('paymentAmountTax').get('raw'):
                lst_tax = res_dict.get('paymentAmountTax').get('parsed')
                if lst_tax:
                    tax_amount = lst_tax
                    # tax_amount = parsed_dict.get('itemTaxRateBeta').get('parsed').replace('%','')
                    if tax_amount:
                        paymentAmountTax = self.env['account.tax'].sudo().search(
                            [('amount', '=', float(tax_amount)), ('type_tax_use', '=', 'sale'),
                             ('amount_type', '=', 'percent'), ('company_id', '=', self.company_id.id)],limit=1)
                        if not paymentAmountTax:
                            paymentAmountTax = self.env['account.tax'].sudo().create({
                                'name': 'Tax ' + res_dict.get('paymentAmountTax').get('raw'),
                                'amount_type': 'percent',
                                'type_tax_use': 'sale',
                                'amount': float(tax_amount),
                                'company_id': self.company_id.id
                            })
                if paymentAmountTax:
                    for line in move_lines:
                        line_tax_ids = line.get('tax_ids') or []
                        line_tax_ids.append((4, paymentAmountTax.id))
                        line.update({'tax_ids': line_tax_ids})
            else:
                lst_tax = res_dict.get('paymentAmountTax').get('parsed')
                if lst_tax:
                    tax_amount = float(lst_tax)
                    if tax_amount:
                        total = sum([line.get('price_unit')*line.get('quantity') for line in move_lines])
                        if total:
                            for line in move_lines:
                                sub_total = line.get('price_unit')*line.get('quantity')
                                sub_total_per = (sub_total*100)/total

                                tax_amt = ((sub_total_per*tax_amount)/100)/line.get('quantity')

                                paymentAmountTax = self.env['account.tax'].sudo().search(
                                    [('amount', '=', float(tax_amt)),
                                     ('type_tax_use', '=', 'sale'),
                                     ('amount_type', '=', 'fixed'), ('company_id', '=', self.company_id.id)],limit=1)

                                if not paymentAmountTax:
                                    paymentAmountTax = self.env['account.tax'].sudo().create({
                                        'name': 'Tax ' + str(tax_amt),
                                        'amount_type': 'fixed',
                                        'type_tax_use': 'sale',
                                        'amount': float(tax_amt),
                                        'company_id': self.company_id.id
                                    })
                                if paymentAmountTax:
                                    line_tax_ids = line.get('tax_ids') or []
                                    line_tax_ids.append((4, paymentAmountTax.id))
                                    line.update({'tax_ids': line_tax_ids})

        return move_lines

    def action_create_invoice(self):
        res_dict = ast.literal_eval(self.document_response)
        if not res_dict:
            raise UserError(_("Data Not Found!"))
        partner = self.get_partner_move(res_dict)
        if not partner:
            raise UserError(_("Customer details not found in data. it's mandatory for create invoice and receipt!"))
        invoice_line = self.parepare_move_line(res_dict)

        currency_id = False
        if 'currencyCode' in res_dict and res_dict.get('currencyCode'):
            currency_id = self.env['res.currency'].sudo().search([('name','=',res_dict.get('currencyCode').get('parsed').get('value'))])

        invoice_date = False
        if 'invoiceDate' in res_dict and res_dict.get('invoiceDate'):
            invoice_date = res_dict.get('invoiceDate').get('parsed')

        invoice_date_due = False
        if 'paymentDateDue' in res_dict and res_dict.get('paymentDateDue'):
            invoice_date_due = res_dict.get('paymentDateDue').get('parsed')

        move_vals = {
            'partner_id' : partner.id,
            'invoice_date' : invoice_date,
            'invoice_date_due' : invoice_date_due,
            'currency_id' : currency_id.id if currency_id else self.company_id.currency_id.id,
            'company_id': self.company_id.id,
            'invoice_line_ids': [(0, 0, line) for line in invoice_line]

        }

        if self.extractor == 'invoice':
            move_vals.update({
                'move_type': 'out_invoice',
            })
        if self.extractor == 'receipt':
            move_vals.update({
                'move_type': 'in_receipt',
            })
        if self.extractor == 'credit-note':
            move_vals.update({
                'move_type': 'out_refund',
            })

        move = self.env['account.move'].sudo().create(move_vals)
        self.move_id = move.id

    @api.onchange('affinda_workspace_collection')
    def onchange_affinda_workspace_collection(self):
        if self.affinda_workspace_collection:
            self.affinda_workspace = self.affinda_workspace_collection.affinda_workspace.id
        else:
            self.affinda_workspace = False

    def action_create_document(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key:
                url = self.company_id.affinda_api_url + "/documents"
                headers = {
                    "Authorization": "Bearer " + self.company_id.affinda_api_key,
                    "Content-Type": "application/json",
                }

                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

                attch_url = base_url + "/web/content/" + str(self.attachment_id.id)
                _logger.info('Url >>>... %s ',attch_url)
                payload = {
                    'url' : attch_url,
                    'collection' : self.affinda_workspace_collection.identifier,
                    'workspace' : self.affinda_workspace.identifier,
                }
                try:
                    response = requests.post(url,json=payload, headers=headers)
                except requests.exceptions.ConnectionError:
                    raise UserError(
                        ("please check your internet connection."))
                if response.status_code == 200:
                    response_dict = json.loads(response.text)
                    self.write({
                        'document_response': response_dict.get('data'),
                        'identifier':response_dict.get('meta',False).get('identifier',False) if response_dict.get('meta',False) else False,
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))

    def action_get_document(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key and self.identifier:
                url = self.company_id.affinda_api_url + "/documents/" + self.identifier
                headers = {
                    "Authorization": "Bearer " + self.company_id.affinda_api_key,
                    "Content-Type": "application/json",
                }
                try:
                    response = requests.get(url, headers=headers)
                except requests.exceptions.ConnectionError:
                    raise UserError(
                        ("please check your internet connection."))
                if response.status_code == 200:
                    response_dict = json.loads(response.text)
                    self.write({
                        'document_response': response_dict.get('data'),
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))

    def action_delete_document(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key and self.identifier:
                url = self.company_id.affinda_api_url + "/documents/" + self.identifier
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
                        'document_response': False,
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))

