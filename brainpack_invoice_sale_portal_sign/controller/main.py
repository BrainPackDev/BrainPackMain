import binascii

from odoo import http, _, fields
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.sale.controllers.portal import CustomerPortal


class InvoiceSignature(http.Controller):

    @http.route(['/my/invoices/<int:invoice_id>/accept'], type='json', auth="public", website=True)
    def portal_invoice_sign(self, invoice_id, signature=None):
        try:
            invoice_sudo = request.env['account.move'].sudo().browse(invoice_id)
        except (AccessError, MissingError):
            return {'error': _('Invalid invoice.')}
        attachment = request.env['ir.attachment'].sudo().create({
            'name': invoice_sudo.name + '/' + invoice_sudo.partner_id.name + ' /Signature',
            'type': 'binary',
            'datas': signature
        })

        invoice_sudo.sudo().write({
            'signature_attachment': attachment.id
        })
        return {
            'force_refresh': True
        }

    @http.route(['/my/orders/<int:order_id>/sign'], type='json', auth="public", website=True)
    def portal_quote_sign(self, order_id, access_token=None, name=None, signature=None, company_name=None, company_number=None):
        try:
            order_sudo = request.env['sale.order'].sudo().browse(order_id)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        try:
            order_sudo.sudo().write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
                'sign_company_name': company_name,
                'sign_company_number': company_number,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo._has_to_be_paid():
            order_sudo.sudo().action_confirm()
            order_sudo.sudo()._send_order_confirmation_mail()

        query_string = '&message=sign_ok'
        if order_sudo.sudo()._has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }

class CustomerPortal(CustomerPortal):
    @http.route(['/my/orders/<int:order_id>/accept'], type='json', auth="public", website=True)
    def portal_quote_accept(self, order_id, access_token=None, name=None, signature=None, company_name=None, company_number=None, behalf_of_company= None):
        # get from query string if not on json param
        access_token = access_token or request.httprequest.args.get('access_token')
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return {'error': _('Invalid order.')}

        if not order_sudo._has_to_be_signed():
            return {'error': _('The order is not in a state requiring customer signature.')}
        if not signature:
            return {'error': _('Signature is missing.')}

        try:
            order_sudo.write({
                'signed_by': name,
                'signed_on': fields.Datetime.now(),
                'signature': signature,
                'sign_company_name': company_name,
                'sign_company_number': company_number,
                'behalf_of_company': behalf_of_company,
            })
            request.env.cr.commit()
        except (TypeError, binascii.Error) as e:
            return {'error': _('Invalid signature data.')}

        if not order_sudo._has_to_be_paid():
            order_sudo.action_confirm()
            order_sudo._send_order_confirmation_mail()

        pdf = request.env['ir.actions.report'].sudo()._render_qweb_pdf('sale.action_report_saleorder', [order_sudo.id])[
            0]

        _message_post_helper(
            'sale.order',
            order_sudo.id,
            _('Order signed by %s', name),
            attachments=[('%s.pdf' % order_sudo.name, pdf)],
            token=access_token,
        )

        query_string = '&message=sign_ok'
        if order_sudo._has_to_be_paid(True):
            query_string += '#allow_payment=yes'
        return {
            'force_refresh': True,
            'redirect_url': order_sudo.get_portal_url(query_string=query_string),
        }


