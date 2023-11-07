# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo import http
from odoo.addons.brainpack_mobile_app.controllers.controller import WebServiceMobile

from odoo import registry as registry_get
import logging
import json
from odoo.http import content_disposition, request
_logger = logging.getLogger(__name__)

mime = 'text/xml'
class DeviceDetails(WebServiceMobile):

    # @http.route('/api/v1/remove/notification/<int:id>', csrf=False, type='json', auth='none', methods=['POST'])
    # def remove_notification(self, **kwargs):
    #     uid = kwargs.get('id')
    #     response = self._authenticate()
    #     response.update({'request_type': "POST"})
    #     request_data = http.request.jsonrequest
    #     if response.get("success"):
    #         verify_acess = self._verify_access_token(
    #             uid, request_data.get('access_token'))
    #         if not verify_acess.get('status'):
    #             response.update({
    #                 "success": False,
    #                 "key_token": False,
    #                 "success_msg": "Invalid Key token",
    #                 'err_msg': "Invalid Request"
    #             })
    #             return self._response("dynamic_route", response, self.ctype)
    #         context = {}
    #         db_name = tools.config['db_name']
    #         registry = registry_get(db_name)
    #         with registry.cursor() as cr:
    #             env = api.Environment(cr, SUPERUSER_ID, context)
    #             try:
    #                 user_id = request_data.get('user_id')
    #                 notification_id = request_data.get('notification_id')
    #                 user_id = env['res.users'].sudo().search([('id', '=', user_id)])
    #                 if user_id:
    #                     notifi_id = env['app.push.notification'].sudo().search([('id', '=', int(notification_id))], limit=1)
    #                     if not notifi_id:
    #                         response.update({
    #                             "success": False,
    #                             "success_msg": "Notification not found.",
    #                             'status': '0',
    #                             "key_token": True,
    #                             'user_id': uid,
    #                             'access_token': request_data.get('access_token'),
    #                         })
    #                     else:
    #                         notifi_id = env['app.push.notification'].sudo().search(
    #                             [('active_users_ids', 'in', user_id.ids), ('id', '=', notifi_id.id)], limit=1)
    #                         notifi_id.active_users_ids = [(3 , user_id.id)]
    #                     response.update({
    #                         "success": True,
    #                         "success_msg": "Remove Notification.",
    #                         'status': '1',
    #                         "key_token": True,
    #                         'user_id': uid,
    #                         'access_token': request_data.get('access_token'),
    #                     })
    #                 else:
    #                     response.update({
    #                         "success": False,
    #                         "success_msg": "User not found.",
    #                         'status': '0',
    #                         "key_token": True,
    #                         'user_id': uid,
    #                         'access_token': request_data.get('access_token'),
    #                     })
    #             except Exception as e:
    #                 response = self.exception_response_update(response, uid, e)
    #     else:
    #         response = self.false_response_update(
    #             response, uid, request_data.get('access_token'))
    #     return self._response("dynamic_route", response, self.ctype)
    #
    # @http.route('/api/v1/sent/notification/<int:id>', csrf=False, type='json', auth='none', methods=['POST'])
    # def sent_notification_history(self, **kwargs):
    #     uid = kwargs.get('id')
    #     response = self._authenticate()
    #     response.update({'request_type': "POST"})
    #     request_data = http.request.jsonrequest
    #     if response.get("success"):
    #         verify_acess = self._verify_access_token(
    #             uid, request_data.get('access_token'))
    #         if not verify_acess.get('status'):
    #             response.update({
    #                 "success": False,
    #                 "key_token": False,
    #                 "success_msg": "Invalid Key token",
    #                 'err_msg': "Invalid Request"
    #             })
    #             return self._response("dynamic_route", response, self.ctype)
    #         context = {}
    #         db_name = tools.config['db_name']
    #         registry = registry_get(db_name)
    #         with registry.cursor() as cr:
    #             env = api.Environment(cr, SUPERUSER_ID, context)
    #             try:
    #                 user_id = request_data.get('user_id')
    #                 user_id = env['res.users'].sudo().search([('id', '=', user_id)])
    #                 _logger.info("\n\n -------- USer id  - %s ", user_id)
    #                 if user_id:
    #                     notifi_ids = env['app.push.notification'].sudo().search([('active_users_ids', 'in', user_id.ids)])
    #                     notification_data = []
    #                     for notifi_id in notifi_ids:
    #                         notification_data.append({
    #                             'id': notifi_id.id,
    #                             'title': notifi_id.app_notification_title,
    #                             'message': notifi_id.message,
    #                             'image_url':notifi_id.app_notification_image,
    #                             'date': notifi_id.notification_send_datetime,
    #                             })
    #                     response.update({
    #                         "success": True,
    #                         "notification_data": notification_data,
    #                         "success_msg": "Notification details updated.",
    #                         'status': '1',
    #                         "key_token": True,
    #                         'user_id': uid,
    #                         'access_token': request_data.get('access_token'),
    #                     })
    #                 else:
    #                     response.update({
    #                         "success": True,
    #                         "success_msg": "Notification not found.",
    #                         'status': '0',
    #                         "key_token": True,
    #                         'user_id': uid,
    #                         'access_token': request_data.get('access_token'),
    #                     })
    #             except Exception as e:
    #                 response = self.exception_response_update(response, uid, e)
    #     else:
    #         response = self.false_response_update(
    #             response, uid, request_data.get('access_token'))
    #     return self._response("dynamic_route", response, self.ctype)

    @http.route('/api/v1/add/device_details/<int:id>', csrf=False, type='json', auth='none', methods=['POST'], cors="*")
    def add_device_details(self, **kwargs):
        uid = kwargs.get('id')
        # response = self._authenticate()
        self._mData = request.httprequest.data and json.loads(
            request.httprequest.data.decode('utf-8')) or {}
        self.ctype = request.httprequest.headers.get(
            'Content-Type') == mime and mime or 'json'
        self.header = request.httprequest.headers
        response = {}
        response.update({'request_type': "POST"})
        request_data = self._mData
        if self._mData:
            verify_acess = self._verify_access_token(
                uid, request_data.get('access_token'))
            if not verify_acess.get('status'):
                response.update({
                    "success": False,
                    "key_token": False,
                    "success_msg": "Invalid Key token",
                    'err_msg': "Invalid Request"
                })
                return self._response("dynamic_route", response, self.ctype)
            context = {}
            db_name = tools.config['db_name']
            registry = registry_get(db_name)
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, context)
                try:
                    user_id = request_data.get('user_id')
                    user_id = env['res.users'].sudo().search([('id', '=', user_id)])
                    if user_id:
                        user_id.write({
                            'device_type': request_data.get('device_type'),
                            'unique_id': request_data.get('unique_id'),
                            'mo_app_version': request_data.get('mo_app_version'),
                            'fcm_token': request_data.get('fcm_token'),
                        })
                        response.update({
                            "success": True,
                            "success_msg": "User device details updated.",
                            'status': '1',
                            "key_token": True,
                            'user_id': uid,
                            'access_token': request_data.get('access_token'),
                        })
                    else:
                        response.update({
                            "success": True,
                            "success_msg": "User not found.",
                            'status': '0',
                            "key_token": True,
                            'user_id': uid,
                            'access_token': request_data.get('access_token'),
                        })
                except Exception as e:
                    response = self.exception_response_update(response, uid, e)
        else:
            response.update({
                'status': 'Fail',
                'message': 'Data not found.'
            })
        return self._response("dynamic_route", response, self.ctype)
