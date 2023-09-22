import requests
from odoo import _, api, fields, models, tools

from odoo.exceptions import UserError
import json


class Provider(models.Model):
    _inherit = 'provider'

    def send_mpm_template(self, template, language, namespace, partner, params):
        t = type(self)
        fn = getattr(t, f'{self.provider}_send_mpm_template', None)
        res = fn(self, template, language, namespace, partner, params)
        return res

    def direct_send_mpm_template(self, template, language, namespace, mobile, params):
        t = type(self)
        fn = getattr(t, f'{self.provider}_direct_send_mpm_template', None)
        res = fn(self, template, language, namespace, mobile, params)
        return res

    def graph_api_direct_send_mpm_template(self, template, language, namespace, partner, params):
        if self.graph_api_authenticated:
            url = self.graph_api_url + self.graph_api_instance_id + "/messages"
            header_text = False
            header = {}
            wa_template_id = self.env['wa.template'].search([('name', '=', template)]) or self.env.context.get('wa_template')
            # context_wa_template_id = self.env.context.get('wa_template')
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'header'):
                if any(i.get('type') == 'header' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'header'][0].get('parameters')[0].get('type') == 'text':
                        header_text = [i for i in params if i.get('type') == 'header'][0].get('parameters')[0].get(
                            'text')
                        header.update({"type": "text",
                                       "text": header_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'header').formate == 'text':
                        header_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'header').text
                        header.update({"type": "text",
                                       "text": header_text})
            body_text = False
            body = {}
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'body'):
                if any(i.get('type') == 'body' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'body'][0].get('parameters')[0].get('type') == 'text':
                        body_text = [i for i in params if i.get('type') == 'body'][0].get('parameters')[0].get('text')
                        body.update({"type": "text",
                                     "text": body_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'body'):
                        body_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'body').text
                        body.update({"text": body_text})

            footer_text = False
            footer = {}
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'footer'):
                if any(i.get('type') == 'footer' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'footer'][0].get('parameters')[0].get('type') == 'text':
                        footer_text = [i for i in params if i.get('type') == 'footer'][0].get('parameters')[0].get(
                            'text')
                        footer.update({"type": "text",
                                       "text": footer_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'footer'):
                        footer_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'footer').text
                        footer.update({"text": footer_text})
            template_type = wa_template_id.components_ids.filtered(
                lambda x: x.type == 'interactive').type
            interactive_type = wa_template_id.components_ids.filtered(
                lambda x: x.type == 'interactive').interactive_type

            interactive_product = False
            if interactive_type == 'product' or interactive_type == 'button':
                interactive_product = {
                    "type": interactive_type,
                    "body": body or '',
                    "action": params[0]
                }
            if interactive_type == 'product_list':
                interactive_product = {
                    "type": interactive_type,
                    "header": header or '',
                    "body": body or '',
                    "action": params[0]
                }
            if interactive_type == 'list':
                interactive_product = {
                    "type": interactive_type,
                    "header": header or '',
                    "body": body or '',
                    "footer": footer or '',
                    "action": params[0]
                }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": partner.phone,
                "type": template_type,
                "interactive": interactive_product
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.graph_api_token
            }
            try:
                answer = requests.post(url, headers=headers, data=payload)
            except requests.exceptions.ConnectionError:
                raise UserError(
                    ("please check your internet connection."))
            if answer.status_code != 200:
                if json.loads(answer.text) and 'error' in json.loads(answer.text) and 'message' in json.loads(
                        answer.text).get('error'):
                    dict = json.loads(answer.text).get('error').get('message')
                    raise UserError(_(dict))
            return answer
        else:
            raise UserError(
                ("please authenticated your whatsapp."))

    def graph_api_send_mpm_template(self, template, language, namespace, partner, params):
        if self.graph_api_authenticated:
            url = self.graph_api_url + self.graph_api_instance_id + "/messages"
            header_text = False
            header = {}
            wa_template_id = self.env['wa.template'].search([('name', '=', template)]) or self.env.context.get('wa_template')
            # context_wa_template_id = self.env.context.get('wa_template')
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'header'):
                if any(i.get('type') == 'header' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'header'][0].get('parameters')[0].get('type') == 'text':
                        header_text = [i for i in params if i.get('type') == 'header'][0].get('parameters')[0].get(
                            'text')
                        header.update({"type": "text",
                                       "text": header_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'header').formate == 'text':
                        header_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'header').text
                        header.update({"type": "text",
                                       "text": header_text})
            body_text = False
            body = {}
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'body'):
                if any(i.get('type') == 'body' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'body'][0].get('parameters')[0].get('type') == 'text':
                        body_text = [i for i in params if i.get('type') == 'body'][0].get('parameters')[0].get('text')
                        body.update({"type": "text",
                                     "text": body_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'body'):
                        body_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'body').text
                        body.update({"text": body_text})

            footer_text = False
            footer = {}
            if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'footer'):
                if any(i.get('type') == 'footer' for i in params if 'type' in i):
                    if [i for i in params if i.get('type') == 'footer'][0].get('parameters')[0].get('type') == 'text':
                        footer_text = [i for i in params if i.get('type') == 'footer'][0].get('parameters')[0].get(
                            'text')
                        footer.update({"type": "text",
                                       "text": footer_text})
                else:
                    if wa_template_id and wa_template_id.components_ids.filtered(lambda x: x.type == 'footer'):
                        footer_text = wa_template_id.components_ids.filtered(
                            lambda x: x.type == 'footer').text
                        footer.update({"text": footer_text})
            template_type = wa_template_id.components_ids.filtered(
                lambda x: x.type == 'interactive').type
            interactive_type = wa_template_id.components_ids.filtered(
                lambda x: x.type == 'interactive').interactive_type

            interactive_product = False
            if interactive_type == 'product' or interactive_type == 'button':
                interactive_product = {
                    "type": interactive_type,
                    "body": body or '',
                    "action": params[0]
                }
            if interactive_type == 'product_list':
                interactive_product = {
                    "type": interactive_type,
                    "header": header or '',
                    "body": body or '',
                    "action": params[0]
                }
            if interactive_type == 'list':
                interactive_product = {
                    "type": interactive_type,
                    "header": header or '',
                    "body": body or '',
                    "footer": footer or '',
                    "action": params[0]
                }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": partner.mobile,
                "type": template_type,
                "interactive": interactive_product
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.graph_api_token
            }
            try:
                answer = requests.post(url, headers=headers, data=payload)
            except requests.exceptions.ConnectionError:
                raise UserError(
                    ("please check your internet connection."))
            if answer.status_code != 200:
                if json.loads(answer.text) and 'error' in json.loads(answer.text) and 'message' in json.loads(
                        answer.text).get('error'):
                    dict = json.loads(answer.text).get('error').get('message')
                    raise UserError(_(dict))
            return answer
        else:
            raise UserError(
                ("please authenticated your whatsapp."))
