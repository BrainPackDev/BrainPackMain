from io import BytesIO
import requests
from PIL import Image
from odoo.osv import expression
import random
import string
import werkzeug
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo import http
import json
import xml.etree.ElementTree as ET
from ast import literal_eval
from odoo import registry as registry_get
import re
import logging
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import content_disposition, request
import base64
from datetime import datetime
default_token_size = 16
_logger = logging.getLogger(__name__)
invalid_request_string = "Invalid Request"

mime = 'text/xml'

def _default_unique_key(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

class WebServiceMobile(http.Controller):
    def _authenticate(self):
        """ Helps to authenticate the user returns success true or false using access_token gotten from login api
            uses _auth fn and verify_request fn"""
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        self.auth = request.httprequest.headers.get("Authorization")
        user_id = self._mData.get('user_id')

        return self._auth()

    def verify_request(self, webservice_id):
        webservice = request.env['webservice.account'].sudo().browse([
            webservice_id])
        algo = webservice.algo
        hash_val = webservice.get_hash()
        _logger.info("***********hash_val******",hash_val)
        if 'auth' in dir(self) and self.auth and hash_val == self.auth.encode('ascii'):
            return {"success": True, "message": "API Authorization Successful"}
        else:
            return {"success": False, "message": "API Invalid Authorization:%r" % self.auth}

    def _auth(self):
        webservice_id = request.env['res.config.settings'].sudo(
        )._default_webservice()
        if webservice_id:
            res = self.verify_request(webservice_id)
        else:
            res = {"success": False, "message": "EndPoint not Found.", }
        return res

    @http.route('/api/v1/login', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def prolitus_login(self, **kwargs):
        _logger.info("***********/api/v1/login api started******")
        # response = self._authenticate(
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        # response.update({'request_type': "POST"})
        request_data = self._mData
        # if response.get("success") and request_data:
        db_name = tools.config['db_name']
        try:
            request.session.authenticate(str(db_name), str(
                request_data.get('login')), str(request_data.get('password')))
            session_info = request.env['ir.http'].session_info()
            _logger.info("==LOGIN REQUESTED==",)
            user_secert = request.env['user.login.secret'].sudo().search(
                [('user_id', '=', session_info['uid'])], limit=1)
            if not user_secert:
                user_secert = request.env['user.login.secret'].sudo().create({
                    'user_id': session_info['uid'],
                    'access_token': _default_unique_key(default_token_size)
                })
            else:
                user_secert.write({
                    'access_token': _default_unique_key(default_token_size)
                })

            resuser = request.env['res.users'].sudo()
            user_id = resuser.browse(
                [int(session_info['uid'])])

            menu_items = []
            menu_records = request.env['ir.ui.menu'].search(
                [('parent_id', '=', False)])
            for menu in menu_records:
                menu_items.append({
                    'menu_name': menu.complete_name,
                    'menu_id': menu.id,
                    'main_menu': True if menu.complete_name == 'Discuss' else False,
                    'icon_image': 'data:image/png;base64,'+menu.web_icon_data.decode('utf-8') if menu.web_icon_data else False,
                })
            response.update({
                "success": True,
                "key_token": True,
                "success_msg": "Valid Key token",
                'user_id': session_info['uid'],
                'access_token': user_secert.access_token,
                'status': '0',
                'menu_items':menu_items,
            })
        except Exception as e:

            _logger.info("==LOGIN FAILED=={}".format(e))
            response.update({
                "success": False,
                "key_token": False,
                "success_msg": "Invalid Key token",
                'status': '1',
                'user_id': False
            })
        # else:
        #     uid = False
        #     access_token = False
        #     response = self.false_response_update(response, uid, access_token)
        _logger.info("***********/api/v1/login api ended******")
        return self._response("dynamic_route", response, self.ctype)

    def _verify_access_token(self, user_id=False, token=False):
        result = {'status': False}
        user_secert = request.env['user.login.secret'].sudo().search(
            [('user_id', '=', user_id), ('access_token', '=', token)], limit=1)
        if user_secert:
            result = {
                'status': True
            }
        return result

    def false_response_update(self, response, uid, access_token):
        response.update({
            "success": False,
            'status': '1',
            "key_token": True,
            "success_msg": "Valid Key token",
            'user_id': uid,
        })
        if uid:
            verify_acess = self._verify_access_token(
                uid, access_token)
            if not verify_acess.get('status'):
                response.update({
                    "success": False,
                    "key_token": False,
                    "success_msg": "Invalid Key token",
                    'err_msg': "Invalid Request"
                })
        return response

    def _response(self, apiname, response, ctype='json'):
        if response.get('object_id'):
            response.pop('object_id')
        if ctype == 'json':
            if response.get('request_type') == 'GET':
                return werkzeug.wrappers.Response(json.dumps(response), headers=[('Content-Type', 'application/json')],
                                                  status=200)
            else:
                return response
        else:
            body = self._wrap2xml(apiname, response)
        headers = [
            ('Content-Type', mime),
            ('Content-Length', len(body))
        ]
        return werkzeug.wrappers.Response(body, headers=headers)

    @http.route('/api/v1/get/channels/<int:user_id>', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def get_channel_data(self, user_id=False, **kwargs):
        if not user_id:
            user_id = kwargs.get('user_id')
        uid = user_id
        # response = self._authenticate()
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        response.update({'request_type': "POST"})
        request_data = self._mData

        if not request_data:
            return {
                'status': 'Fail',
                'message': 'Data not found.'
            }

        verify_access = self._verify_access_token(
            request_data.get('user_id'), request_data.get('access_token'))
        if not verify_access.get('status'):
            response.update(
                {"success": False, "key_token": False, "success_msg": "Invalid Key token",
                 'err_msg': invalid_request_string})
            return self._response("dynamic_route", response, self.ctype)
        env = api.Environment(request.cr, uid, request.env.context)

        part = request.env['res.users'].browse(int(user_id)).partner_id
        channels_data = []
        channels = request.env['mail.channel'].search([('channel_partner_ids', 'in', [part.id]),('active','=',True),('channel_type','in',['channel','chat', 'group'])])
        # self.channel_member_ids.filtered(lambda member: not member.is_pinned)
        for channel in channels:
            if channel.sudo().channel_member_ids.filtered(lambda member: member.is_pinned and member.partner_id == part):
                persona_member = channel.sudo().channel_member_ids.filtered(lambda member:member.partner_id != part)
                channel_display_name = channel.name
                if channel.channel_type == 'chat':
                    if len(persona_member) == 1:
                        channel_display_name = persona_member.custom_channel_name or persona_member.partner_id.name
                if channel.channel_type == 'group':
                    channel_display_name = ','.join([member.custom_channel_name or member.partner_id.name or '' for member in channel.sudo().channel_member_ids])

                channel_data_dict = (channel.sudo().with_user(user_id).channel_info_custom()[0])
                channel_data_dict.update({
                    'channel_display_name': channel_display_name
                })
                channels_data.append(channel_data_dict)

        for channel in channels_data:
            if channel.get('last_message_id'):
                message_id = request.env['mail.message'].sudo().browse(channel.get('last_message_id'))
                channel.update({'date':message_id.create_date})
            else:
                channel_write_date = request.env['mail.channel'].sudo().browse(channel.get('id')).write_date
                channel.update({'date': channel_write_date})

        channels_data = sorted(channels_data, key=lambda i: i['date'], reverse=True)


        if not channels_data:
            return {
                'status': 'Fail',
                'message': 'Channels data not found.'
            }
        else:

            return {
                "success": True,
                "success_msg": "Channel data found!",
                'channels_data': channels_data
            }
        return {
            "success": False,
            "success_msg": "Invalid Key token",
            'error_msg': 'Password Do not match'
        }

    @http.route('/api/v1/get/messages', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def get_messages_data(self, **kwargs):
        # response = self._authenticate()
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        response.update({'request_type': "POST"})
        if self._mData:
            request_data = self._mData
            verify_access = self._verify_access_token(
                request_data.get('user_id'), request_data.get('access_token'))
            if not verify_access.get('status'):
                response.update({
                    "success": False,
                    "key_token": False,
                    "success_msg": "Invalid Key token",
                    'err_msg': invalid_request_string
                })
                return self._response("dynamic_route", response, self.ctype)
            if request_data.get('channel_id'):
                channel_id = request_data.get('channel_id')
                pagination = request_data.get('pagination') or 1
                if pagination and pagination > 0:
                    pagination = pagination - 1
                    user_partner = request.env['res.users'].browse(request_data.get('user_id')).partner_id
                    channel_member_sudo = request.env['mail.channel.member'].sudo().search([('channel_id', '=', channel_id), ('partner_id', '=', user_partner.id)], limit=1)
                    domain = [
                        ('res_id', '=', channel_id),
                        ('model', '=', 'mail.channel'),
                        ('message_type', '!=', 'user_notification'),
                    ]
                    if 'chat' in request_data and request_data.get('chat') == 'whatsapp':
                        domain.append(('message_type','=','wa_msgs'))
                    else:
                        domain.append(('message_type', '=', 'comment'))

                    fields = channel_member_sudo.env['mail.message'].sudo()._get_message_format_fields()
                    fields.append('parent_id')
                    fields.append('attachment_ids')

                    messages_data = channel_member_sudo.env['mail.message'].sudo().with_user(
                        request_data.get('user_id')).search_read(domain, fields=fields, offset=pagination*30, limit=30)

                    if not messages_data:
                        return {
                            'status': 'Fail',
                            'message': 'Messages data not found.'
                        }

                    for message in messages_data:
                        if message.get('parent_id'):
                            parent_message_data = channel_member_sudo.env['mail.message'].sudo().with_user(
                                request_data.get('user_id')).search_read([('id','=',message.get('parent_id')[0])], fields=fields)
                            message.update({
                                'parent_id':parent_message_data
                            })

                        if message.get('attachment_ids'):
                            attachment_data = request.env['ir.attachment'].sudo().search_read([('id','in',message.get('attachment_ids'))],['name','datas','type','mimetype'])
                            message.update({
                                'attachment_ids': attachment_data
                            })

                    response.update({
                        "success": True,
                        "success_msg": "Messages data found!",
                        'status': "1",
                        'messages_data':messages_data,
                    })
                    return response
                else:
                    response.update(
                        {"success": False, "key_token": True, "success_msg": "Valid Key token", 'status': "2"})
            else:
                response.update(
                    {"success": False, "key_token": True, "success_msg": "Channel Not Found in Paramater!", 'status': "2"})
        else:
            response.update({
                'status': 'Fail',
                'message': 'Data not found.'
            })
        _logger.info("*****************messages api ended**")
        return self._response("dynamic_route", response, self.ctype)

    @http.route('/api/v1/get/frame_url', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def get_iframe_url(self, **kwargs):
        # response = self._authenticate()
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        response.update({'request_type': "POST"})
        if self._mData:
            request_data = self._mData
            verify_access = self._verify_access_token(
                request_data.get('user_id'), request_data.get('access_token'))
            if not verify_access.get('status'):
                response.update({
                    "success": False,
                    "key_token": False,
                    "success_msg": "Invalid Key token",
                    'err_msg': invalid_request_string
                })
                return self._response("dynamic_route", response, self.ctype)
            if request_data.get('menu_id'):
                menu = request.env['ir.ui.menu'].with_user(request_data.get('user_id')).search([('id', '=', request_data.get('menu_id'))])
                if menu:
                    base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    url = base_url + "/web#menu_id=" + str(request_data.get('menu_id'))
                    response.update({
                        "success": True,
                        "success_msg": "Url Get Successfully!",
                        'status': "1",
                        'frame_url': url,
                    })
                else:
                    response.update(
                        {"success": False, "key_token": True, "success_msg": "Menu Id Not Found On System!", 'status': "2"})
        else:
            response.update({
                'status': 'Fail',
                'message': 'Data not found.'
            })
        return self._response("dynamic_route", response, self.ctype)

    @http.route('/api/v1/send/message', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def send_message(self, **kwargs):
        # response = self._authenticate()
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        response.update({'request_type': "POST"})
        if self._mData:
            request_data = self._mData
            verify_access = self._verify_access_token(
                request_data.get('user_id'), request_data.get('access_token'))
            if not verify_access.get('status'):
                response.update({
                    "success": False,
                    "key_token": False,
                    "success_msg": "Invalid Key token",
                    'err_msg': invalid_request_string
                })
                return self._response("dynamic_route", response, self.ctype)
            body = request_data.get('body',False)
            if not body:
                body = ' '
            if request_data.get('channel_id') and body:
                channel_id = request_data.get('channel_id')
                channel_obj = request.env['mail.channel'].sudo().with_user(request_data.get('user_id')).search([('id','=',channel_id)])
                user_obj = request.env['res.users'].sudo().browse(request_data.get('user_id'))
                body = request_data.get('body')

                if channel_obj:
                    message_values = {
                        'body': body,
                        'author_id': user_obj.partner_id.id,
                        'email_from': user_obj.partner_id.email or '',
                        'model': 'mail.channel',
                        'subtype_id': request.env['ir.model.data'].sudo()._xmlid_to_res_id('mail.mt_comment'),
                        'partner_ids': [(4, user_obj.partner_id.id)],
                        'res_id': channel_id,
                        'reply_to': user_obj.partner_id.email,
                        'attachment_ids' :[]
                    }
                    if 'chat' in request_data and request_data.get('chat') == 'whatsapp':
                        message_values.update({'message_type':'wa_msgs'})
                    else:
                        message_values.update({'message_type':'comment'})

                    if request_data.get('attachments',[]):
                        for attachment in request_data.get('attachments'):
                            list_attachments = []
                            if attachment.get('name') and attachment.get('datas') and attachment.get('type') and attachment.get('mimetype'):
                                attachment_value = {
                                    'name': attachment.get('name') or 'BrainPack',
                                    'datas': attachment.get('datas') or '',
                                    'type': attachment.get('type') or '',
                                    'mimetype': attachment.get('mimetype'),
                                }
                                list_attachments.append(attachment_value)
                            else:
                                response.update(
                                    {"success": False, "key_token": True, "success_msg": "Required Parameter For Attachment Missing! (name, datas, type(url, binary), mimetype)",
                                     'status': "2"})
                                return self._response("dynamic_route", response, self.ctype)


                        attachment_obj = request.env['ir.attachment'].sudo().with_user(request_data.get('user_id')).create(list_attachments)
                        message_values.get('attachment_ids').append((6,0, attachment_obj.ids))

                    if 'parent_id' in request_data and request_data.get('parent_id') and request.env['mail.message'].sudo().search([('id','=',request_data.get('parent_id'))]):
                        message_values.update({'parent_id': request_data.get('parent_id')})

                    message_obj = request.env['mail.message'].sudo().with_user(request_data.get('user_id')).create(
                        message_values)
                    notifications = channel_obj._channel_message_notifications(message_obj)
                    request.env['bus.bus']._sendmany(notifications)

                    fields = request.env['mail.message'].sudo()._get_message_format_fields()
                    fields.append('parent_id')
                    message_data = request.env['mail.message'].sudo().search_read([('id','=',message_obj.id)],fields=fields)

                    for message in message_data:
                        if message.get('parent_id'):
                            parent_message_data = request.env['mail.message'].sudo().with_user(
                                request_data.get('user_id')).search_read([('id','=',message.get('parent_id')[0])], fields=fields)
                            message.update({
                                'parent_id':parent_message_data
                            })

                    response.update({
                        "success": True,
                        "success_msg": "Messages Created Sucessfully!",
                        'status': "1",
                        'messages_data': message_data,
                    })
                    return response
                else:
                    response.update(
                        {"success": False, "key_token": True, "success_msg": "Channel Not Available in System!", 'status': "2"})
            else:
                response.update(
                    {"success": False, "key_token": True, "success_msg": "Required Parameter Missing! (Channel Id)",
                     'status': "2"})
        else:
            response.update({
                'status': 'Fail',
                'message': 'Data not found.'
            })
        _logger.info("*****************messages api ended**")
        return self._response("dynamic_route", response, self.ctype)