# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http, fields, _
from odoo.exceptions import UserError
import math
from odoo.tools.safe_eval import safe_eval
import uuid
import json
from datetime import datetime


def generate_slider_tab_token():
    ran_num = str(uuid.uuid4().int)
    token = int(ran_num[:5] + ran_num[-5:])
    return str(token)


class blog_slider(http.Controller):

  
    # ===============================
    # theme 14 template 10 blog 14
    # ===============================
  
    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_pets_10_tab_pane_layout', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_tmpl_pets_10_tab_pane_layout(self, slider_id=False):
        data = """
                <div class="row js_cls_corpomate_blog_slider_main_div_10">
                
                </div>        
        """

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)

        if not slider_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id', '=', slider_id),
        ], limit=1)

        # #######################
        # BLOG TYPE SLIDER
        # #######################
        if slider:

            # NOTE: HARDCODED FOR BLOG 10 THEME 10 ONLY
            is_show_tab_local = False

            # ========================================
            # NAV ITEMS
            # ========================================
            nav_tabs = ''
            list_nav_items = []
            nav_item_id_token_pair_dic = {}
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                    }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                    })

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_pets_10_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })

#             nav_tabs = nav_tabs.decode("utf-8")

            # ========================================
            # NAV ITEMS
            # ========================================

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id)
                    }

                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                                'author_name': blog_post.sudo().author_id.sudo().name if blog_post.sudo().author_id.sudo() else '',
                            }

                            list_blog_posts.append(blog_post_dic)

                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False
                        filter_domain = [
                            ('website_id', 'in', (False, website_id)),
                            ('website_published', '=', True),
                        ]

                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit

                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(
                                tab_pane.filter_id.sudo().domain)
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)

                        blog_posts = request.env['blog.post'].sudo().search(
                            filter_domain, order=sort, limit=limit)

                        if blog_posts:
                            for blog_post in blog_posts:

                                cover_properties = json.loads(
                                    blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)

                                post_date_month_name = dt.strftime("%B")
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y")

                                blog_post_href = '/blog/%s/post/%s' % (
                                    blog_post.blog_id.id, blog_post.id)
                                blog_post_dic = {
                                    'name': blog_post.name,
                                    'blog_post_href': blog_post_href,
                                    'img_src': cover_properties.get('background-image', False),
                                    'cover_properties': cover_properties,
                                    'subtitle': blog_post.subtitle or '',
                                    'post_date': post_date,
                                    'post_date_month_name': post_date_month_name,
                                    'post_date_month_day': post_date_month_day,
                                    'author_name': blog_post.sudo().author_id.sudo().name if blog_post.sudo().author_id.sudo() else '',
                                }

                                list_blog_posts.append(blog_post_dic)

                    tab_pane_dic.update({
                        'list_blog_posts': list_blog_posts
                    })

#                     is_first_tab_with_products = False
                    # ==================================
                    # No TAB THINGS
                    if is_show_tab_local:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True

                    # No TAB THINGS
                    # ==================================

                    list_tab_pane.append(tab_pane_dic)

            # ==================================
            # NO TAB THINGS
            if not is_show_tab_local:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get(
                            "list_blog_posts", [])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(
                                    item_blog_post_dic)

                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                    })
                    one_tab_pane.append(list_tab_pane_single_dic)

                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_pets_10_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
            })
#             tab_pane = tab_pane.decode("utf-8")

            data = """
                    <div class="row js_cls_corpomate_blog_slider_main_div_10">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs': nav_tabs,
                'tab_pane': tab_pane,
            }

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values  

# ================================================================================
    # ================================================================================
    # theme 4 template 10 blog 4
    # ================================================================================
    # ================================================================================

    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_transport_tmpl_10_tab_pane_layout', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_transport_tmpl_10_tab_pane_layout(self, slider_id=False):
        data = """
                <div class="row js_cls_corpomate_blog_slider_main_div_4">
                
                </div>        
        """

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)

        if not slider_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id', '=', slider_id),
        ], limit=1)

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################
        if slider:

            # NOTE: HARDCODED FOR BLOG 17 THEME 17 ONLY
            is_show_tab_local = False

            # ========================================
            # NAV ITEMS
            # ========================================
            nav_tabs = ''
            list_nav_items = []
            nav_item_id_token_pair_dic = {}
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                    }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                    })

            template_id = "sh_corpomate_theme.sh_corpomate_theme_transport_tmpl_10_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })

#             nav_tabs = nav_tabs.decode("utf-8")

            # ========================================
            # NAV ITEMS
            # ========================================

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id)
                    }

                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                                'author_name': blog_post.sudo().author_id.sudo().name if blog_post.sudo().author_id.sudo() else '',
                            }

                            list_blog_posts.append(blog_post_dic)

                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False
                        filter_domain = [
                            ('website_id', 'in', (False, website_id)),
                            ('website_published', '=', True),
                        ]

                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit

                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(
                                tab_pane.filter_id.sudo().domain)
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)

                        blog_posts = request.env['blog.post'].sudo().search(
                            filter_domain, order=sort, limit=limit)

                        if blog_posts:
                            for blog_post in blog_posts:

                                cover_properties = json.loads(
                                    blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)

                                post_date_month_name = dt.strftime("%B")
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y")

                                blog_post_href = '/blog/%s/post/%s' % (
                                    blog_post.blog_id.id, blog_post.id)
                                blog_post_dic = {
                                    'name': blog_post.name,
                                    'blog_post_href': blog_post_href,
                                    'img_src': cover_properties.get('background-image', False),
                                    'cover_properties': cover_properties,
                                    'subtitle': blog_post.subtitle or '',
                                    'post_date': post_date,
                                    'post_date_month_name': post_date_month_name,
                                    'post_date_month_day': post_date_month_day,
                                    'author_name': blog_post.sudo().author_id.sudo().name if blog_post.sudo().author_id.sudo() else '',
                                }

                                list_blog_posts.append(blog_post_dic)

                    tab_pane_dic.update({
                        'list_blog_posts': list_blog_posts
                    })

#                     is_first_tab_with_products = False
                    # ==================================
                    # No TAB THINGS
                    if is_show_tab_local:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True

                    # No TAB THINGS
                    # ==================================

                    list_tab_pane.append(tab_pane_dic)

            # ==================================
            # NO TAB THINGS
            if not is_show_tab_local:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get(
                            "list_blog_posts", [])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(
                                    item_blog_post_dic)

                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                    })
                    one_tab_pane.append(list_tab_pane_single_dic)

                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS

            template_id = "sh_corpomate_theme.sh_corpomate_theme_transport_tmpl_10_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
            })
#             tab_pane = tab_pane.decode("utf-8")

            data = """
                    <div class="row our-blog js_cls_corpomate_blog_slider_main_div_4">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs': nav_tabs,
                'tab_pane': tab_pane,
            }

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values

  # ================================================================================
    # ================================================================================
    # theme 4 template 10 blog 4
    # ================================================================================
    # ================================================================================






    

    # Blog 2 template 8

    # ======================================================================================
    # ======================================================================================
    # ======================================================================================
    # ######################################################################################

    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_crypto_8_tab_pane_one', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_tmpl_crypto_8_tab_pane_one(self, tab_id=False, token=False):
        data = ''

        if tab_id and type(tab_id) != int:
            tab_id = int(tab_id)

        if not tab_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        tab_obj = request.env["sh.corpomate.blog.slider.tab.blog.post.line"]

        tab_pane = tab_obj.search([
            ('id', '=', tab_id),
        ], limit=1)

        slider = False
        if tab_pane:
            slider = tab_pane.slider_id

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################
        if slider:

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if tab_pane:
                tab_pane_dic = {
                    'id': tab_pane.id,
                    'name': tab_pane.name,
                    'id_tab_pane': 'nav_tab_' + token
                }

                list_blog_posts = []
                if slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                    for blog_post in tab_pane.blog_post_ids:

                        cover_properties = json.loads(
                            blog_post.cover_properties)
                        dt = datetime.date(blog_post.post_date)

                        post_date_month_name = dt.strftime("%B")
                        post_date_month_day = dt.strftime("%d")
                        post_date = dt.strftime("%d %B %Y")

                        blog_post_href = '/blog/%s/post/%s' % (
                            blog_post.blog_id.id, blog_post.id)
                        blog_post_dic = {
                            'name': blog_post.name,
                            'blog_post_href': blog_post_href,
                            'img_src': cover_properties.get('background-image', False),
                            'cover_properties': cover_properties,
                            'subtitle': blog_post.subtitle or '',
                            'post_date': post_date,
                            'post_date_month_name': post_date_month_name,
                            'post_date_month_day': post_date_month_day,
                        }

                        list_blog_posts.append(blog_post_dic)

                elif slider.filter_type == 'domain':
                    # IF DOMAIN

                    website_id = request.website.id if request.website else False
                    filter_domain = [
                        ('website_id', 'in', (False, website_id)),
                        ('website_published', '=', True),
                    ]

                    sort = []
                    limit = None
                    if tab_pane.limit > 0:
                        limit = tab_pane.limit

                    if tab_pane.filter_id.sudo():
                        filter_domain += safe_eval(
                            tab_pane.filter_id.sudo().domain)
                        sort = safe_eval(tab_pane.filter_id.sudo().sort)

                    blog_posts = request.env['blog.post'].sudo().search(
                        filter_domain, order=sort, limit=limit)

                    if blog_posts:
                        for blog_post in blog_posts:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                            }

                            list_blog_posts.append(blog_post_dic)

                tab_pane_dic.update({
                    'list_blog_posts': list_blog_posts
                })

                list_tab_pane.append(tab_pane_dic)

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_crypto_8_tab_pane_one"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,

            })
#             tab_pane = tab_pane.decode("utf-8")

            data = tab_pane

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values

    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_crypto_8_tab_pane_layout', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_tmpl_crypto_8_tab_pane_layout(self, slider_id=False):
        data = """
                <div class="card js_cls_corpomate_blog_slider_main_div_2">
                
                </div>        
        """

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)

        if not slider_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id', '=', slider_id),
        ], limit=1)

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################
        if slider:

            # ========================================
            # NAV ITEMS
            # ========================================
            list_nav_items = []
            nav_item_id_token_pair_dic = {}
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                    }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                    })

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_crypto_8_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })

#             nav_tabs = nav_tabs.decode("utf-8")

            # ========================================
            # NAV ITEMS
            # ========================================

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id)
                    }

                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                            }

                            list_blog_posts.append(blog_post_dic)

                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False
                        filter_domain = [
                            ('website_id', 'in', (False, website_id)),
                            ('website_published', '=', True),
                        ]

                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit

                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(
                                tab_pane.filter_id.sudo().domain)
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)

                        blog_posts = request.env['blog.post'].sudo().search(
                            filter_domain, order=sort, limit=limit)

                        if blog_posts:
                            for blog_post in blog_posts:

                                cover_properties = json.loads(
                                    blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)

                                post_date_month_name = dt.strftime("%B")
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y")

                                blog_post_href = '/blog/%s/post/%s' % (
                                    blog_post.blog_id.id, blog_post.id)
                                blog_post_dic = {
                                    'name': blog_post.name,
                                    'blog_post_href': blog_post_href,
                                    'img_src': cover_properties.get('background-image', False),
                                    'cover_properties': cover_properties,
                                    'subtitle': blog_post.subtitle or '',
                                    'post_date': post_date,
                                    'post_date_month_name': post_date_month_name,
                                    'post_date_month_day': post_date_month_day,
                                }

                                list_blog_posts.append(blog_post_dic)

                    tab_pane_dic.update({
                        'list_blog_posts': list_blog_posts
                    })

#                     is_first_tab_with_products = False
                    # ==================================
                    # No TAB THINGS
                    if slider.is_show_tab:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True

                    # No TAB THINGS
                    # ==================================

                    list_tab_pane.append(tab_pane_dic)

            # ==================================
            # NO TAB THINGS
            if not slider.is_show_tab:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get(
                            "list_blog_posts", [])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(
                                    item_blog_post_dic)

                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                    })
                    one_tab_pane.append(list_tab_pane_single_dic)

                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_crypto_8_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
            })
#             tab_pane = tab_pane.decode("utf-8")

            data = """
                    <div class="card js_cls_corpomate_blog_slider_main_div_2">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs': nav_tabs,
                'tab_pane': tab_pane,
            }

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values


# ================================================================================
    # ================================================================================    
    # theme 2 template 482 
    # ================================================================================
    # ================================================================================  
    # ######################################################################################
    # ======================================================================================
    # ======================================================================================
    # ======================================================================================
        # theme -1  Blog 1 template 1

    # ======================================================================================
    # ======================================================================================
    # ======================================================================================
    # ######################################################################################

    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_accounting_11_tab_pane_one', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_tmpl_accounting_11_tab_pane_one(self, tab_id=False, token=False):
        data = ''

        if tab_id and type(tab_id) != int:
            tab_id = int(tab_id)

        if not tab_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        tab_obj = request.env["sh.corpomate.blog.slider.tab.blog.post.line"]

        tab_pane = tab_obj.search([
            ('id', '=', tab_id),
        ], limit=1)

        slider = False
        if tab_pane:
            slider = tab_pane.slider_id

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################
        if slider:

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if tab_pane:
                tab_pane_dic = {
                    'id': tab_pane.id,
                    'name': tab_pane.name,
                    'id_tab_pane': 'nav_tab_' + token
                }

                list_blog_posts = []
                if slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                    for blog_post in tab_pane.blog_post_ids:

                        cover_properties = json.loads(
                            blog_post.cover_properties)
                        dt = datetime.date(blog_post.post_date)

                        post_date_month_name = dt.strftime("%B")
                        post_date_month_day = dt.strftime("%d")
                        post_date = dt.strftime("%d %B %Y")

                        blog_post_href = '/blog/%s/post/%s' % (
                            blog_post.blog_id.id, blog_post.id)
                        blog_post_dic = {
                            'name': blog_post.name,
                            'blog_post_href': blog_post_href,
                            'img_src': cover_properties.get('background-image', False),
                            'cover_properties': cover_properties,
                            'subtitle': blog_post.subtitle or '',
                            'post_date': post_date,
                            'post_date_month_name': post_date_month_name,
                            'post_date_month_day': post_date_month_day,
                        }

                        list_blog_posts.append(blog_post_dic)

                elif slider.filter_type == 'domain':
                    # IF DOMAIN

                    website_id = request.website.id if request.website else False
                    filter_domain = [
                        ('website_id', 'in', (False, website_id)),
                        ('website_published', '=', True),
                    ]

                    sort = []
                    limit = None
                    if tab_pane.limit > 0:
                        limit = tab_pane.limit

                    if tab_pane.filter_id.sudo():
                        filter_domain += safe_eval(
                            tab_pane.filter_id.sudo().domain)
                        sort = safe_eval(tab_pane.filter_id.sudo().sort)

                    blog_posts = request.env['blog.post'].sudo().search(
                        filter_domain, order=sort, limit=limit)

                    if blog_posts:
                        for blog_post in blog_posts:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                            }

                            list_blog_posts.append(blog_post_dic)

                tab_pane_dic.update({
                    'list_blog_posts': list_blog_posts
                })

                list_tab_pane.append(tab_pane_dic)

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_accounting_11_tab_pane_one"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,

            })
#             tab_pane = tab_pane.decode("utf-8")

            data = tab_pane

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values

    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_accounting_11_tab_pane_layout', type='json', auth="none", methods=['post'], website=True)
    def sh_corpomate_theme_tmpl_accounting_11_tab_pane_layout(self, slider_id=False):
        data = """
                <div class="card js_cls_corpomate_blog_slider_main_div_1">
                
                </div>        
        """

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)

        if not slider_id:
            return {}

        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id', '=', slider_id),
        ], limit=1)

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################
        if slider:

            # ========================================
            # NAV ITEMS
            # ========================================
            list_nav_items = []
            nav_item_id_token_pair_dic = {}
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                    }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                    })

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_accounting_11_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })

#             nav_tabs = nav_tabs.decode("utf-8")

            # ========================================
            # NAV ITEMS
            # ========================================

            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id)
                    }

                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:

                            cover_properties = json.loads(
                                blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)

                            post_date_month_name = dt.strftime("%B")
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y")

                            blog_post_href = '/blog/%s/post/%s' % (
                                blog_post.blog_id.id, blog_post.id)
                            blog_post_dic = {
                                'name': blog_post.name,
                                'blog_post_href': blog_post_href,
                                'img_src': cover_properties.get('background-image', False),
                                'cover_properties': cover_properties,
                                'subtitle': blog_post.subtitle or '',
                                'post_date': post_date,
                                'post_date_month_name': post_date_month_name,
                                'post_date_month_day': post_date_month_day,
                            }

                            list_blog_posts.append(blog_post_dic)

                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False
                        filter_domain = [
                            ('website_id', 'in', (False, website_id)),
                            ('website_published', '=', True),
                        ]

                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit

                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(
                                tab_pane.filter_id.sudo().domain)
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)

                        blog_posts = request.env['blog.post'].sudo().search(
                            filter_domain, order=sort, limit=limit)

                        if blog_posts:
                            for blog_post in blog_posts:

                                cover_properties = json.loads(
                                    blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)

                                post_date_month_name = dt.strftime("%B")
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y")

                                blog_post_href = '/blog/%s/post/%s' % (
                                    blog_post.blog_id.id, blog_post.id)
                                blog_post_dic = {
                                    'name': blog_post.name,
                                    'blog_post_href': blog_post_href,
                                    'img_src': cover_properties.get('background-image', False),
                                    'cover_properties': cover_properties,
                                    'subtitle': blog_post.subtitle or '',
                                    'post_date': post_date,
                                    'post_date_month_name': post_date_month_name,
                                    'post_date_month_day': post_date_month_day,
                                }

                                list_blog_posts.append(blog_post_dic)

                    tab_pane_dic.update({
                        'list_blog_posts': list_blog_posts
                    })

#                     is_first_tab_with_products = False
                    # ==================================
                    # No TAB THINGS
                    if slider.is_show_tab:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True

                    # No TAB THINGS
                    # ==================================

                    list_tab_pane.append(tab_pane_dic)

            # ==================================
            # NO TAB THINGS
            if not slider.is_show_tab:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get(
                            "list_blog_posts", [])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(
                                    item_blog_post_dic)

                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                    })
                    one_tab_pane.append(list_tab_pane_single_dic)

                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS

            template_id = "sh_corpomate_theme.sh_corpomate_theme_tmpl_accounting_11_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
            })
#             tab_pane = tab_pane.decode("utf-8")

            data = """
                    <div class="card js_cls_corpomate_blog_slider_main_div_1">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs': nav_tabs,
                'tab_pane': tab_pane,
            }

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################

        values = {
            'data': data
        }

        if slider:
            values.update({
                'items':    slider.items,
                'autoplay': slider.autoplay,
                'speed':    slider.speed,
                'loop':     slider.loop,
                'nav':      slider.nav,
            })

        return values


    # ================================================================================
    # ================================================================================    
    # theme 1 template 11
    # ================================================================================
    # ================================================================================ 



    # ================================================================================
    # ================================================================================    
    # theme-6  template 6 blog 6
    # ================================================================================
    # ================================================================================        
    
    
    
    
    
    
    
    
    
    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_cyber_tmpl_11_tab_pane_one', type='json', auth="none", methods = ['post'], website = True)                  
    def sh_corpomate_theme_cyber_tmpl_11_tab_pane_one(self, tab_id = False,token = False):   
        data = ''




        if tab_id and type(tab_id) != int:
            tab_id = int(tab_id)
            
        if not tab_id:
            return {}
        
                
        slider_obj = request.env["sh.corpomate.blog.slider"]
        tab_obj = request.env["sh.corpomate.blog.slider.tab.blog.post.line"]
        
        
        
                
        tab_pane = tab_obj.search([
            ('id','=',tab_id),
            ],limit = 1)
   
        slider = False
        if tab_pane:
            slider = tab_pane.slider_id
                     

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################        
        if slider:
            
             
            
            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if tab_pane:
                tab_pane_dic = {
                    'id': tab_pane.id,
                    'name': tab_pane.name,
                    'id_tab_pane': 'nav_tab_' + token
                    }
                    
                 
                 
                list_blog_posts = []
                if slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                    for blog_post in tab_pane.blog_post_ids:
                                   
                        cover_properties = json.loads(blog_post.cover_properties)
                        dt = datetime.date(blog_post.post_date)   
                                           
                        post_date_month_name = dt.strftime("%B")
                        post_date_month_name_short = dt.strftime("%b")                        
                        post_date_month_day = dt.strftime("%d")
                        post_date = dt.strftime("%d %B %Y") 
                                                           
                        blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                        blog_post_dic = {
                            'name':blog_post.name,
                            'blog_post_href':blog_post_href,
                            'img_src':cover_properties.get('background-image',False),
                            'cover_properties':cover_properties,
                            'subtitle': blog_post.subtitle or '',                                  
                            'post_date':post_date,     
                            'post_date_month_name':post_date_month_name,
                            'post_date_month_name_short':post_date_month_name_short,
                            'post_date_month_day':post_date_month_day,   
                            'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                     
                        }
                        
                        list_blog_posts.append(blog_post_dic)
                
                
                elif slider.filter_type == 'domain':
                    # IF DOMAIN

                    website_id = request.website.id if request.website else False                          
                    filter_domain = [
                        ('website_id', 'in', (False, website_id )),
                        ('website_published', '=', True),                    
                    ]          
                        
                    sort = []
                    limit = None
                    if tab_pane.limit > 0:
                        limit = tab_pane.limit
                                                                                             
                    if tab_pane.filter_id.sudo():
                        filter_domain += safe_eval(tab_pane.filter_id.sudo().domain)  
                        sort = safe_eval(tab_pane.filter_id.sudo().sort)                        
                    
                    blog_posts = request.env['blog.post'].sudo().search(filter_domain, order = sort, limit = limit)
                    
                    if blog_posts:
                        for blog_post in blog_posts:                        

                            cover_properties = json.loads(blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)   
                                               
                            post_date_month_name = dt.strftime("%B")
                            post_date_month_name_short = dt.strftime("%b")                                
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y") 
                                                               
                            blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                            blog_post_dic = {
                                'name':blog_post.name,
                                'blog_post_href':blog_post_href,
                                'img_src':cover_properties.get('background-image',False),
                                'cover_properties':cover_properties,
                                'subtitle': blog_post.subtitle or '',                                  
                                'post_date':post_date,     
                                'post_date_month_name':post_date_month_name,
                                'post_date_month_name_short':post_date_month_name_short,
                                'post_date_month_day':post_date_month_day,    
                                'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                        
                            }
                            
                            list_blog_posts.append(blog_post_dic)                 
                 
                    
                    
                    
                                                        
                tab_pane_dic.update({
                    'list_blog_posts':list_blog_posts
                })
                
                list_tab_pane.append(tab_pane_dic)
                    
            template_id = "sh_corpomate_theme.sh_corpomate_theme_cyber_tmpl_11_tab_pane_one"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
                                                                
            })        
            # tab_pane = tab_pane.decode("utf-8") 
            
            data = tab_pane
            
        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################             
        
        values = {
            'data':data
            }
               
        if slider:
            values.update({
            'items':    slider.items,
            'autoplay': slider.autoplay,
            'speed':    slider.speed,
            'loop':     slider.loop,
            'nav':      slider.nav,
            })
            
        

      
        return values   




    
    
    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_cyber_tmpl_11_tab_pane_layout', type='json', auth="none", methods = ['post'], website = True)
    def sh_corpomate_theme_cyber_tmpl_11_tab_pane_layout(self, slider_id = False):                    
        data = """
                <div class="card js_cls_corpomate_blog_slider_main_div_6">
                
                </div>        
        """ 
            
            

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)
            
        if not slider_id:
            return {}
        
        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id','=',slider_id),
            ],limit = 1)
   
   

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################        
        if slider:
            
            # ========================================
            # NAV ITEMS
            # ========================================
            list_nav_items = []
            nav_item_id_token_pair_dic = {}            
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()                    
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                        }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                        })
                                
            
            template_id = "sh_corpomate_theme.sh_corpomate_theme_cyber_tmpl_11_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })        
              
            # nav_tabs = nav_tabs.decode("utf-8")
            
            # ========================================
            # NAV ITEMS
            # ========================================
              
            
            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id) 
                        }
                        
                        
                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:
                            
                            cover_properties = json.loads(blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)   
                                               
                            post_date_month_name = dt.strftime("%B")
                            post_date_month_name_short = dt.strftime("%b")                                
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y") 
                                                               
                            blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                            blog_post_dic = {
                                'name':blog_post.name,
                                'blog_post_href':blog_post_href,
                                'img_src':cover_properties.get('background-image',False),
                                'cover_properties':cover_properties,
                                'subtitle': blog_post.subtitle or '',                                  
                                'post_date':post_date,     
                                'post_date_month_name':post_date_month_name,
                                'post_date_month_name_short':post_date_month_name_short,
                                'post_date_month_day':post_date_month_day,   
                                    'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                         
                            }
                            
                            list_blog_posts.append(blog_post_dic)    
                    
                    
                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False                          
                        filter_domain = [
                            ('website_id', 'in', (False, website_id )),
                            ('website_published', '=', True),                    
                        ]          
                                                
                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit
                                                                                                 
                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(tab_pane.filter_id.sudo().domain)  
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)                        
                        
                        blog_posts = request.env['blog.post'].sudo().search(filter_domain, order = sort, limit = limit)
                        
                        if blog_posts:
                            for blog_post in blog_posts:                        
                                
                                cover_properties = json.loads(blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)   
                                                   
                                post_date_month_name = dt.strftime("%B")
                                post_date_month_name_short = dt.strftime("%b")                                    
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y") 
                                                                   
                                blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                                blog_post_dic = {
                                    'name':blog_post.name,
                                    'blog_post_href':blog_post_href,
                                    'img_src':cover_properties.get('background-image',False),
                                    'cover_properties':cover_properties,
                                    'subtitle': blog_post.subtitle or '',                                  
                                    'post_date':post_date,     
                                    'post_date_month_name':post_date_month_name,
                                    'post_date_month_name_short':post_date_month_name_short,
                                    'post_date_month_day':post_date_month_day,   
                                    'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                             
                                }
                                
                                list_blog_posts.append(blog_post_dic)                             
                        
                        
                                                            
                    tab_pane_dic.update({
                        'list_blog_posts':list_blog_posts
                    })
                    
#                     is_first_tab_with_products = False
                    #==================================
                    # No TAB THINGS
                    if slider.is_show_tab:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True
                        
                    # No TAB THINGS
                    #==================================

                    list_tab_pane.append(tab_pane_dic)
            
            # ==================================
            # NO TAB THINGS
            if not slider.is_show_tab:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get("list_blog_posts",[])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(item_blog_post_dic)
                                                     
                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                        })
                    one_tab_pane.append(list_tab_pane_single_dic)
                 
                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS
                        
                                
            template_id = "sh_corpomate_theme.sh_corpomate_theme_cyber_tmpl_11_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,                             
            })        
            # tab_pane = tab_pane.decode("utf-8") 
            
            data = """
                    <div class="card js_cls_corpomate_blog_slider_main_div_6">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs':nav_tabs,
                'tab_pane':tab_pane,
                }
            
        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################             
        
        values = {
            'data':data
            }
               
        if slider:
            values.update({
            'items':    slider.items,
            'autoplay': slider.autoplay,
            'speed':    slider.speed,
            'loop':     slider.loop,
            'nav':      slider.nav,
            })
            
                           
        return values        
    





  # ================================================================================
    # ================================================================================    
    # theme 6 template 6 blog 6
    # ================================================================================
    # ================================================================================  
    # ######################################################################################
    # ======================================================================================




     # ================================================================================
    # ================================================================================    
    # theme-7  template 7 blog 7
    # ================================================================================
    # ================================================================================        
    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_onemate_snippet_tmpl_10_tab_pane_one', type='json', auth="none", methods = ['post'], website = True)                  
    def sh_onemate_snippet_tmpl_10_tab_pane_one(self, tab_id = False,token = False):   
        data = ''




        if tab_id and type(tab_id) != int:
            tab_id = int(tab_id)
            
        if not tab_id:
            return {}
        
                
        slider_obj = request.env["sh.corpomate.blog.slider"]
        tab_obj = request.env["sh.corpomate.blog.slider.tab.blog.post.line"]
        
        
        
                
        tab_pane = tab_obj.search([
            ('id','=',tab_id),
            ],limit = 1)
   
        slider = False
        if tab_pane:
            slider = tab_pane.slider_id
                     

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################        
        if slider:
            
             
            
            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if tab_pane:
                tab_pane_dic = {
                    'id': tab_pane.id,
                    'name': tab_pane.name,
                    'id_tab_pane': 'nav_tab_' + token
                    }
                    
                 
                 
                list_blog_posts = []
                if slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                    for blog_post in tab_pane.blog_post_ids:
                                   
                        cover_properties = json.loads(blog_post.cover_properties)
                        dt = datetime.date(blog_post.post_date)   
                                           
                        post_date_month_name = dt.strftime("%B")
                        post_date_month_name_short = dt.strftime("%b")                        
                        post_date_month_day = dt.strftime("%d")
                        post_date = dt.strftime("%d %B %Y") 
                                                           
                        blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                        blog_post_dic = {
                            'name':blog_post.name,
                            'blog_post_href':blog_post_href,
                            'img_src':cover_properties.get('background-image',False),
                            'cover_properties':cover_properties,
                            'subtitle': blog_post.subtitle or '',                                  
                            'post_date':post_date,     
                            'post_date_month_name':post_date_month_name,
                            'post_date_month_name_short':post_date_month_name_short,
                            'post_date_month_day':post_date_month_day,   
                            'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                     
                        }
                        
                        list_blog_posts.append(blog_post_dic)
                
                
                elif slider.filter_type == 'domain':
                    # IF DOMAIN

                    website_id = request.website.id if request.website else False                          
                    filter_domain = [
                        ('website_id', 'in', (False, website_id )),
                        ('website_published', '=', True),                    
                    ]          
                        
                    sort = []
                    limit = None
                    if tab_pane.limit > 0:
                        limit = tab_pane.limit
                                                                                             
                    if tab_pane.filter_id.sudo():
                        filter_domain += safe_eval(tab_pane.filter_id.sudo().domain)  
                        sort = safe_eval(tab_pane.filter_id.sudo().sort)                        
                    
                    blog_posts = request.env['blog.post'].sudo().search(filter_domain, order = sort, limit = limit)
                    
                    if blog_posts:
                        for blog_post in blog_posts:                        

                            cover_properties = json.loads(blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)   
                                               
                            post_date_month_name = dt.strftime("%B")
                            post_date_month_name_short = dt.strftime("%b")                                
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y") 
                                                               
                            blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                            blog_post_dic = {
                                'name':blog_post.name,
                                'blog_post_href':blog_post_href,
                                'img_src':cover_properties.get('background-image',False),
                                'cover_properties':cover_properties,
                                'subtitle': blog_post.subtitle or '',                                  
                                'post_date':post_date,     
                                'post_date_month_name':post_date_month_name,
                                'post_date_month_name_short':post_date_month_name_short,
                                'post_date_month_day':post_date_month_day,    
                                'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                        
                            }
                            
                            list_blog_posts.append(blog_post_dic)                 
                 
                    
                    
                    
                                                        
                tab_pane_dic.update({
                    'list_blog_posts':list_blog_posts
                })
                
                list_tab_pane.append(tab_pane_dic)
                    
            template_id = "sh_corpomate_theme.sh_onemate_snippet_tmpl_10_tab_pane_one"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,
                                                                
            })        
            # tab_pane = tab_pane.decode("utf-8") 
            
            data = tab_pane
            
        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################             
        
        values = {
            'data':data
            }
               
        if slider:
            values.update({
            'items':    slider.items,
            'autoplay': slider.autoplay,
            'speed':    slider.speed,
            'loop':     slider.loop,
            'nav':      slider.nav,
            })
            
        

      
        return values   




    
    
    @http.route('/sh_corpomate_theme/sh_tab_slider_snippet/sh_onemate_snippet_tmpl_10_tab_pane_layout', type='json', auth="none", methods = ['post'], website = True)
    def sh_onemate_snippet_tmpl_10_tab_pane_layout(self, slider_id = False):                    
        data = """
                <div class="card js_cls_corpomate_blog_slider_main_div_7">
                
                </div>        
        """ 
            
            

        if slider_id and type(slider_id) != int:
            slider_id = int(slider_id)
            
        if not slider_id:
            return {}
        
        slider_obj = request.env["sh.corpomate.blog.slider"]
        slider = slider_obj.search([
            ('id','=',slider_id),
            ],limit = 1)
   
   

        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################        
        if slider:
            
            # ========================================
            # NAV ITEMS
            # ========================================
            list_nav_items = []
            nav_item_id_token_pair_dic = {}            
            if slider and slider.tab_blog_post_line:
                for nav_item in slider.tab_blog_post_line:
                    token = generate_slider_tab_token()                    
                    nav_item_dic = {
                        'id': nav_item.id,
                        'name': nav_item.name,
                        'href': '#nav_tab_' + token
                        }
                    list_nav_items.append(nav_item_dic)
                    nav_item_id_token_pair_dic.update({
                        nav_item.id: token
                        })
                                
            
            template_id = "sh_corpomate_theme.sh_onemate_snippet_tmpl_10_nav_tabs"
            nav_tabs = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_nav_items': list_nav_items,
            })        
              
            # nav_tabs = nav_tabs.decode("utf-8")
            
            # ========================================
            # NAV ITEMS
            # ========================================
              
            
            # ========================================
            # TAB PANE
            # ========================================
            list_tab_pane = []
            if slider and slider.tab_blog_post_line:
                is_first_tab_with_blog_posts = True
                for tab_pane in slider.tab_blog_post_line:
                    tab_pane_dic = {
                        'id': tab_pane.id,
                        'name': tab_pane.name,
                        'id_tab_pane': 'nav_tab_' + nav_item_id_token_pair_dic.get(tab_pane.id) 
                        }
                        
                        
                    list_blog_posts = []
                    if is_first_tab_with_blog_posts and slider.filter_type == 'manual' and tab_pane.blog_post_ids:
                        for blog_post in tab_pane.blog_post_ids:
                            
                            cover_properties = json.loads(blog_post.cover_properties)
                            dt = datetime.date(blog_post.post_date)   
                                               
                            post_date_month_name = dt.strftime("%B")
                            post_date_month_name_short = dt.strftime("%b")                                
                            post_date_month_day = dt.strftime("%d")
                            post_date = dt.strftime("%d %B %Y") 
                                                               
                            blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                            blog_post_dic = {
                                'name':blog_post.name,
                                'blog_post_href':blog_post_href,
                                'img_src':cover_properties.get('background-image',False),
                                'cover_properties':cover_properties,
                                'subtitle': blog_post.subtitle or '',                                  
                                'post_date':post_date,     
                                'post_date_month_name':post_date_month_name,
                                'post_date_month_name_short':post_date_month_name_short,
                                'post_date_month_day':post_date_month_day,   
                                    'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                         
                            }
                            
                            list_blog_posts.append(blog_post_dic)    
                    
                    
                    elif is_first_tab_with_blog_posts and slider.filter_type == 'domain':
                        # IF DOMAIN

                        website_id = request.website.id if request.website else False                          
                        filter_domain = [
                            ('website_id', 'in', (False, website_id )),
                            ('website_published', '=', True),                    
                        ]          
                                                
                        sort = []
                        limit = None
                        if tab_pane.limit > 0:
                            limit = tab_pane.limit
                                                                                                 
                        if tab_pane.filter_id.sudo():
                            filter_domain += safe_eval(tab_pane.filter_id.sudo().domain)  
                            sort = safe_eval(tab_pane.filter_id.sudo().sort)                        
                        
                        blog_posts = request.env['blog.post'].sudo().search(filter_domain, order = sort, limit = limit)
                        
                        if blog_posts:
                            for blog_post in blog_posts:                        
                                
                                cover_properties = json.loads(blog_post.cover_properties)
                                dt = datetime.date(blog_post.post_date)   
                                                   
                                post_date_month_name = dt.strftime("%B")
                                post_date_month_name_short = dt.strftime("%b")                                    
                                post_date_month_day = dt.strftime("%d")
                                post_date = dt.strftime("%d %B %Y") 
                                                                   
                                blog_post_href = '/blog/%s/post/%s' %(blog_post.blog_id.id,blog_post.id)              
                                blog_post_dic = {
                                    'name':blog_post.name,
                                    'blog_post_href':blog_post_href,
                                    'img_src':cover_properties.get('background-image',False),
                                    'cover_properties':cover_properties,
                                    'subtitle': blog_post.subtitle or '',                                  
                                    'post_date':post_date,     
                                    'post_date_month_name':post_date_month_name,
                                    'post_date_month_name_short':post_date_month_name_short,
                                    'post_date_month_day':post_date_month_day,   
                                    'blog_name':blog_post.blog_id.name if blog_post.blog_id else '',                                                                                             
                                }
                                
                                list_blog_posts.append(blog_post_dic)                             
                        
                        
                                                            
                    tab_pane_dic.update({
                        'list_blog_posts':list_blog_posts
                    })
                    
#                     is_first_tab_with_products = False
                    #==================================
                    # No TAB THINGS
                    if slider.is_show_tab:
                        is_first_tab_with_blog_posts = False
                    else:
                        is_first_tab_with_blog_posts = True
                        
                    # No TAB THINGS
                    #==================================

                    list_tab_pane.append(tab_pane_dic)
            
            # ==================================
            # NO TAB THINGS
            if not slider.is_show_tab:
                one_tab_pane = []
                if list_tab_pane:
                    list_tab_pane_single_dic = list_tab_pane[0]
                    list_blog_posts_single = []
                    for item_tab_dic in list_tab_pane:
                        item_blog_post_dic_list = item_tab_dic.get("list_blog_posts",[])
                        if item_blog_post_dic_list:
                            for item_blog_post_dic in item_blog_post_dic_list:
                                list_blog_posts_single.append(item_blog_post_dic)
                                                     
                    list_tab_pane_single_dic.update({
                        "list_blog_posts": list_blog_posts_single
                        })
                    one_tab_pane.append(list_tab_pane_single_dic)
                 
                    list_tab_pane = one_tab_pane
                    nav_tabs = ''
            # ==================================
            # NO TAB THINGS
                        
                                
            template_id = "sh_corpomate_theme.sh_onemate_snippet_tmpl_10_tab_pane"
            tab_pane = request.env["ir.ui.view"]._render_template(template_id, values={
                'list_tab_pane': list_tab_pane,                             
            })        
            # tab_pane = tab_pane.decode("utf-8") 
            
            data = """
                    <div class="card js_cls_corpomate_blog_slider_main_div_7">
                        %(nav_tabs)s
                        %(tab_pane)s
                    
                    </div>
            
            """ % {
                'nav_tabs':nav_tabs,
                'tab_pane':tab_pane,
                }
            
        # #####################################################################
        # BLOG TYPE SLIDER
        # #####################################################################             
        
        values = {
            'data':data
            }
               
        if slider:
            values.update({
            'items':    slider.items,
            'autoplay': slider.autoplay,
            'speed':    slider.speed,
            'loop':     slider.loop,
            'nav':      slider.nav,
            })
            
                           
        return values        
    





  # ================================================================================
    # ================================================================================    
    # theme 7 template 7 blog 7
    # ================================================================================
    # ================================================================================  
    # ######################################################################################
    # ======================================================================================


    