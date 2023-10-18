# from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class CustomerPortalSale(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            if website.company_id != request.env['sale.order'].sudo().browse(order_id).company_id:
                return request.redirect('/my')
        return super(CustomerPortalSale, self).portal_order_page(order_id=order_id, report_type=report_type,
                                                                    access_token=access_token, message=message,
                                                                    download=download, kw=kw)

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            if website.company_id != request.env['account.move'].sudo().browse(invoice_id).company_id:
                return request.redirect('/my')
        return super(CustomerPortalSale, self).portal_my_invoice_detail(invoice_id=invoice_id,  access_token=access_token,report_type=report_type,
                                                                    download=download, kw=kw)

    def _prepare_quotations_domain(self, partner):
        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sent', 'cancel'])
        ]
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id','=',website.company_id.id)]
        return domain

    def _prepare_orders_domain(self, partner):
        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['sale', 'done'])
        ]
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id','=',website.company_id.id)]
        return domain

    def _get_invoices_domain(self):
        domain = [('state', 'not in', ('cancel', 'draft')), (
        'move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt'))]
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id','=',website.company_id.id)]
        return domain
