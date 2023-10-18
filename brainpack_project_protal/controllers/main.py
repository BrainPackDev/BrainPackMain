from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.project.controllers.portal import ProjectCustomerPortal

class ProjectCustomerPortal(ProjectCustomerPortal):

    @http.route(['/my/tasks/<int:task_id>'], type='http', auth="public", website=True)
    def portal_my_task(self, task_id, report_type=None, access_token=None, project_sharing=False, **kw):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            if website.company_id != request.env['project.task'].sudo().browse(task_id).company_id:
                return request.redirect('/my')
        return super().portal_my_task(task_id=task_id, report_type=report_type, access_token=access_token, project_sharing=project_sharing,kw=kw)

    @http.route(['/my/projects/<int:project_id>', '/my/projects/<int:project_id>/page/<int:page>'], type='http',
                auth="public", website=True)
    def portal_my_project(self, project_id=None, access_token=None, page=1, date_begin=None, date_end=None, sortby=None,
                          search=None, search_in='content', groupby=None, task_id=None, **kw):
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            if website.company_id != request.env['project.project'].sudo().browse(project_id).company_id:
                return request.redirect('/my')
        return super().portal_my_project(project_id=project_id,access_token=access_token,page=page,date_begin=date_begin,date_end=date_end,sortby=sortby,search=search,search_in=search_in,groupby=groupby,task_id=task_id,kw=kw)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = []
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id', '=', website.company_id.id)]
        if 'project_count' in counters:
            domain += []
            values['project_count'] = request.env['project.project'].search_count(domain) \
                if request.env['project.project'].check_access_rights('read', raise_exception=False) else 0
        if 'task_count' in counters:
            domain += [('project_id', '!=', False)]
            values['task_count'] = request.env['project.task'].search_count(domain) \
                if request.env['project.task'].check_access_rights('read', raise_exception=False) else 0
        return values

    def _prepare_project_domain(self):
        domain = super()._prepare_project_domain()
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            domain += [('company_id', '=', website.company_id.id)]
        return domain

    def _prepare_tasks_values(self, page, date_begin, date_end, sortby, search, search_in, groupby, url="/my/tasks",
                              domain=None, su=False):
        company_domain = []
        if 'website_id' in request.env.context and request.env.context.get('website_id'):
            website = request.env['website'].sudo().browse(request.env.context.get('website_id'))
            company_domain = [('company_id', '=', website.company_id.id)]
        if not domain:
            domain = company_domain
        else:
            domain += company_domain
        return  super()._prepare_tasks_values(page, date_begin, date_end, sortby, search, search_in, groupby, url="/my/tasks",domain=domain, su=su)