# from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.http import request
from odoo.addons.purchase.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo import fields, http, SUPERUSER_ID, tools, _

class CustomerPortalPurchase(CustomerPortal):

    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            if website.company_id != request.env['purchase.order'].sudo().browse(order_id).company_id:
                return request.redirect('/my')
        return super().portal_my_purchase_order(order_id=order_id,access_token=access_token,kw=kw)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        PurchaseOrder = request.env['purchase.order']
        if 'rfq_count' in counters:
            domain = [
                ('state', 'in', ['sent'])
            ]
            if 'website_id' in request.env.context and request.env.context.get('website_id'):
                website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
                domain += [('company_id', '=', website.company_id.id)]
            values['rfq_count'] = PurchaseOrder.search_count(domain) if PurchaseOrder.check_access_rights('read', raise_exception=False) else 0
        if 'purchase_count' in counters:
            domain = [
                ('state', 'in', ['purchase', 'done', 'cancel'])
            ]
            if 'website_id' in request.env.context and request.env.context.get('website_id'):
                website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
                domain += [('company_id', '=', website.company_id.id)]
            values['purchase_count'] = PurchaseOrder.search_count(domain) if PurchaseOrder.check_access_rights('read', raise_exception=False) else 0
        return values

    def _render_portal(self, template, page, date_begin, date_end, sortby, filterby, domain, searchbar_filters, default_filter, url, history, page_name, key):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id', '=', website.company_id.id)]
        return super()._render_portal(template, page, date_begin, date_end, sortby, filterby, domain, searchbar_filters, default_filter, url, history, page_name, key)