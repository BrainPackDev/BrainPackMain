from odoo import _, api, fields, models, modules, tools
import requests
from odoo.exceptions import UserError
import json

test_dict = {
  'bankAccountNumber': None,
  'bankBsb': None,
  'bankIban': None,
  'bankSortCode': None,
  'bankSwift': None,
  'bpayBillerCode': None,
  'bpayReference': None,
  'currencyCode': {
    'id': 91892883,
    'rectangle': None,
    'rectangles': [

    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'ILS',
    'parsed': {
      'id': 69,
      'label': 'ILS',
      'value': 'ILS',
      'synonyms': None,
      'collection': None,
      'description': None,
      'organization': None
    },
    'confidence': None,
    'classificationConfidence': None,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'JZguvEaB',
    'contentType': 'enum',
    'parent': None
  },
  'customerBillingAddress': {
    'id': 91892841,
    'rectangle': {
      'x0': 28.938334,
      'y0': 220.9361,
      'x1': 120.91979,
      'y1': 257.16968,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 28.938334,
        'y0': 220.9361,
        'x1': 120.91979,
        'y1': 257.16968,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'Tes city Tarapacá 123213 Chile',
    'parsed': {
      'formatted': None,
      'streetNumber': None,
      'street': None,
      'apartmentNumber': None,
      'city': None,
      'postalCode': None,
      'state': None,
      'country': None,
      'rawInput': 'Tes city Tarapacá 123213 Chile',
      'countryCode': None,
      'latitude': None,
      'longitude': None
    },
    'confidence': 0.964,
    'classificationConfidence': 0.964,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'IIrmUFpr',
    'contentType': 'location',
    'parent': None
  },
  'customerBusinessNumber': {
    'id': 91892842,
    'rectangle': {
      'x0': 59.500137,
      'y0': 206.29315,
      'x1': 97.49604,
      'y1': 213.50299,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 59.500137,
        'y0': 206.29315,
        'x1': 97.49604,
        'y1': 213.50299,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '1234567',
    'parsed': '1234567',
    'confidence': 0.902,
    'classificationConfidence': 0.902,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'sQTrimjN',
    'contentType': 'text',
    'parent': None
  },
  'customerCompanyName': {
    'id': 91892843,
    'rectangle': {
      'x0': 29.732218,
      'y0': 188.82288,
      'x1': 173.61119,
      'y1': 200.38727,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 29.732218,
        'y0': 188.82288,
        'x1': 173.61119,
        'y1': 200.38727,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'Etamar Company, Etamar',
    'parsed': 'Etamar Company, Etamar',
    'confidence': 0.969,
    'classificationConfidence': 0.969,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'YCquITSP',
    'contentType': 'text',
    'parent': None
  },
  'customerContactName': None,
  'customerDeliveryAddress': None,
  'customerEmail': None,
  'customerNumber': None,
  'customerPhoneNumber': None,
  'customerVat': None,
  'invoiceDate': {
    'id': 91892844,
    'rectangle': {
      'x0': 293.07248,
      'y0': 188.67004,
      'x1': 360.4007,
      'y1': 198.85895,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 293.07248,
        'y0': 188.67004,
        'x1': 360.4007,
        'y1': 198.85895,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '11/16/2023',
    'parsed': '2023-11-16',
    'confidence': 0.976,
    'classificationConfidence': 0.976,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'sRakysMP',
    'contentType': 'date',
    'parent': None
  },
  'invoiceNumber': {
    'id': 91892845,
    'rectangle': {
      'x0': 199.86053,
      'y0': 80.26367,
      'x1': 283.4602,
      'y1': 91.620056,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 199.86053,
        'y0': 80.26367,
        'x1': 283.4602,
        'y1': 91.620056,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '2023-00044',
    'parsed': '2023-00044',
    'confidence': 0.976,
    'classificationConfidence': 0.976,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'bWFyBeNU',
    'contentType': 'text',
    'parent': None
  },
  'invoiceOrderDate': None,
  'invoicePurchaseOrderNumber': None,
  'openingBalance': None,
  'paymentAmountBase': None,
  'paymentAmountDue': {
    'id': 91892846,
    'rectangle': {
      'x0': 495.408,
      'y0': 446.34213,
      'x1': 558.7743,
      'y1': 462.36838,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 495.408,
        'y0': 446.34213,
        'x1': 558.7743,
        'y1': 462.36838,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '₪ 1.00',
    'parsed': '1.00',
    'confidence': 0.676,
    'classificationConfidence': 0.676,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'hTyimjpc',
    'contentType': 'decimal',
    'parent': None
  },
  'paymentAmountPaid': None,
  'paymentAmountTax': None,
  'paymentAmountTotal': {
    'id': 91892847,
    'rectangle': {
      'x0': 533.8134,
      'y0': 338.91608,
      'x1': 559.73895,
      'y1': 345.76627,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 533.8134,
        'y0': 338.91608,
        'x1': 559.73895,
        'y1': 345.76627,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '₪ 1.00',
    'parsed': '1.00',
    'confidence': 0.659,
    'classificationConfidence': 0.659,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'jeMSNwCq',
    'contentType': 'decimal',
    'parent': None
  },
  'paymentDateDue': {
    'id': 91892848,
    'rectangle': {
      'x0': 293.07248,
      'y0': 231.73022,
      'x1': 360.4007,
      'y1': 241.91913,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 293.07248,
        'y0': 231.73022,
        'x1': 360.4007,
        'y1': 241.91913,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': '11/16/2023',
    'parsed': '2023-11-16',
    'confidence': 0.974,
    'classificationConfidence': 0.974,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'RmsWpucw',
    'contentType': 'date',
    'parent': None
  },
  'paymentDelivery': None,
  'paymentOtherCharges': None,
  'paymentReference': {
    'id': 91892849,
    'rectangle': {
      'x0': 279.5364,
      'y0': 518.45636,
      'x1': 353.57785,
      'y1': 526.21936,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 279.5364,
        'y0': 518.45636,
        'x1': 353.57785,
        'y1': 526.21936,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'INV/2023-00044',
    'parsed': 'INV/2023-00044',
    'confidence': 0.589,
    'classificationConfidence': 0.589,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'CZQkkTuw',
    'contentType': 'text',
    'parent': None
  },
  'paymentTerms': None,
  'supplierAddress': {
    'id': 91892850,
    'rectangle': {
      'x0': 495.23514,
      'y0': 88.51062,
      'x1': 565.8834,
      'y1': 126.529785,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 495.23514,
        'y0': 88.51062,
        'x1': 565.8834,
        'y1': 126.529785,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus',
    'parsed': {
      'formatted': None,
      'streetNumber': None,
      'street': None,
      'apartmentNumber': None,
      'city': None,
      'postalCode': None,
      'state': None,
      'country': None,
      'rawInput': 'Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus',
      'countryCode': None,
      'latitude': None,
      'longitude': None
    },
    'confidence': 0.979,
    'classificationConfidence': 0.979,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'HRTaEvcW',
    'contentType': 'location',
    'parent': None
  },
  'supplierBusinessNumber': {
    'id': 91892851,
    'rectangle': {
      'x0': 502.2946,
      'y0': 74.06183,
      'x1': 564.35254,
      'y1': 81.27167,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 502.2946,
        'y0': 74.06183,
        'x1': 564.35254,
        'y1': 81.27167,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'CY10440092L',
    'parsed': 'CY10440092L',
    'confidence': 0.924,
    'classificationConfidence': 0.924,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'rvshbPQZ',
    'contentType': 'text',
    'parent': None
  },
  'supplierCompanyName': {
    'id': 91892852,
    'rectangle': {
      'x0': 445.0864,
      'y0': 59.38983,
      'x1': 563.24133,
      'y1': 67.075134,
      'pageIndex': 0
    },
    'rectangles': [
      {
        'x0': 445.0864,
        'y0': 59.38983,
        'x1': 563.24133,
        'y1': 67.075134,
        'pageIndex': 0
      }
    ],
    'document': 'zJlGVIfW',
    'pageIndex': 0,
    'raw': 'BrainPack.io / Memetech ltd',
    'parsed': 'BrainPack.io / Memetech ltd',
    'confidence': 0.973,
    'classificationConfidence': 0.973,
    'textExtractionConfidence': 1.0,
    'isVerified': False,
    'isClientVerified': False,
    'isAutoVerified': False,
    'dataPoint': 'rFeFJcwy',
    'contentType': 'text',
    'parent': None
  },
  'supplierEmail': None,
  'supplierFax': None,
  'supplierPhoneNumber': None,
  'supplierVat': None,
  'supplierWebsite': None,
  'tables': None,
  'tablesBeta': [
    {
      'id': 91892853,
      'rectangle': {
        'x0': 30.501642223196722,
        'y0': 300.4959,
        'x1': 565.1140097768033,
        'y1': 319.1043097768033,
        'pageIndex': 0
      },
      'rectangles': [
        {
          'x0': 30.501642223196722,
          'y0': 300.4959,
          'x1': 565.1140097768033,
          'y1': 319.1043097768033,
          'pageIndex': 0
        }
      ],
      'document': 'zJlGVIfW',
      'pageIndex': 0,
      'raw': None,
      'parsed': {
        'rows': [
          {
            'id': 91892869,
            'rectangle': {
              'x0': 30.501642223196722,
              'y0': 300.4959,
              'x1': 565.1140097768033,
              'y1': 319.1043097768033,
              'pageIndex': 0
            },
            'rectangles': [
              {
                'x0': 30.501642223196722,
                'y0': 300.4959,
                'x1': 565.1140097768033,
                'y1': 319.1043097768033,
                'pageIndex': 0
              }
            ],
            'document': 'zJlGVIfW',
            'pageIndex': 0,
            'raw': 'BrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00',
            'parsed': {
              'itemDescriptionBeta': {
                'id': 91892871,
                'rectangle': {
                  'x0': 35.658752,
                  'y0': 305.4959,
                  'x1': 193.48831,
                  'y1': 313.9472,
                  'pageIndex': 0
                },
                'rectangles': [
                  {
                    'x0': 35.658752,
                    'y0': 305.4959,
                    'x1': 193.48831,
                    'y1': 313.9472,
                    'pageIndex': 0
                  }
                ],
                'document': 'zJlGVIfW',
                'pageIndex': 0,
                'raw': 'BrainPack Licensing - Base Cloud Server',
                'parsed': 'BrainPack Licensing - Base Cloud Server',
                'confidence': 0.998,
                'classificationConfidence': 0.998,
                'textExtractionConfidence': 1.0,
                'isVerified': False,
                'isClientVerified': False,
                'isAutoVerified': False,
                'dataPoint': 'arJqZwjI',
                'contentType': 'text',
                'parent': 91892869
              },
              'itemTotalBeta': {
                'id': 91892873,
                'rectangle': {
                  'x0': 533.8134,
                  'y0': 305.55957,
                  'x1': 559.9569,
                  'y1': 312.4098,
                  'pageIndex': 0
                },
                'rectangles': [
                  {
                    'x0': 533.8134,
                    'y0': 305.55957,
                    'x1': 559.9569,
                    'y1': 312.4098,
                    'pageIndex': 0
                  }
                ],
                'document': 'zJlGVIfW',
                'pageIndex': 0,
                'raw': '₪ 1.00',
                'parsed': '1.00',
                'confidence': 0.878,
                'classificationConfidence': 0.878,
                'textExtractionConfidence': 1.0,
                'isVerified': False,
                'isClientVerified': False,
                'isAutoVerified': False,
                'dataPoint': 'KVMQbSOq',
                'contentType': 'decimal',
                'parent': 91892869
              },
              'itemUnitBeta': {
                'id': 91892872,
                'rectangle': {
                  'x0': 361.88202,
                  'y0': 305.55957,
                  'x1': 382.10928,
                  'y1': 312.35516,
                  'pageIndex': 0
                },
                'rectangles': [
                  {
                    'x0': 361.88202,
                    'y0': 305.55957,
                    'x1': 382.10928,
                    'y1': 312.35516,
                    'pageIndex': 0
                  }
                ],
                'document': 'zJlGVIfW',
                'pageIndex': 0,
                'raw': 'Units',
                'parsed': 'Units',
                'confidence': 0.707,
                'classificationConfidence': 0.707,
                'textExtractionConfidence': 1.0,
                'isVerified': False,
                'isClientVerified': False,
                'isAutoVerified': False,
                'dataPoint': 'xuRjCxVR',
                'contentType': 'text',
                'parent': 91892869
              },
              'itemQuantityBeta': {
                'id': 91892874,
                'rectangle': {
                  'x0': 342.66565,
                  'y0': 305.59595,
                  'x1': 359.2116,
                  'y1': 312.35516,
                  'pageIndex': 0
                },
                'rectangles': [
                  {
                    'x0': 342.66565,
                    'y0': 305.59595,
                    'x1': 359.2116,
                    'y1': 312.35516,
                    'pageIndex': 0
                  }
                ],
                'document': 'zJlGVIfW',
                'pageIndex': 0,
                'raw': '1.00',
                'parsed': 1.0,
                'confidence': 0.997,
                'classificationConfidence': 0.997,
                'textExtractionConfidence': 1.0,
                'isVerified': False,
                'isClientVerified': False,
                'isAutoVerified': False,
                'dataPoint': 'LoylITwn',
                'contentType': 'float',
                'parent': 91892869
              },
              'itemUnitPriceBeta': {
                'id': 91892870,
                'rectangle': {
                  'x0': 454.2582,
                  'y0': 305.59595,
                  'x1': 470.80417,
                  'y1': 312.35516,
                  'pageIndex': 0
                },
                'rectangles': [
                  {
                    'x0': 454.2582,
                    'y0': 305.59595,
                    'x1': 470.80417,
                    'y1': 312.35516,
                    'pageIndex': 0
                  }
                ],
                'document': 'zJlGVIfW',
                'pageIndex': 0,
                'raw': '1.00',
                'parsed': '1.00',
                'confidence': 0.997,
                'classificationConfidence': 0.997,
                'textExtractionConfidence': 1.0,
                'isVerified': False,
                'isClientVerified': False,
                'isAutoVerified': False,
                'dataPoint': 'EJQqPpQh',
                'contentType': 'decimal',
                'parent': 91892869
              }
            },
            'confidence': None,
            'classificationConfidence': None,
            'textExtractionConfidence': 1.0,
            'isVerified': False,
            'isClientVerified': False,
            'isAutoVerified': False,
            'dataPoint': 'kCodJrel',
            'contentType': 'group',
            'parent': 91892853
          }
        ]
      },
      'confidence': None,
      'classificationConfidence': None,
      'textExtractionConfidence': 1.0,
      'isVerified': False,
      'isClientVerified': False,
      'isAutoVerified': False,
      'dataPoint': 'ftkJQmWB',
      'contentType': 'table',
      'parent': None
    }
  ],
  'rawText': 'Client Name \nEtamar Company, Etamar \nTax ID 1234567 Tes city Tarapacá 123213 Chile \nINVOICE \n# 2023-00044 \nInvoice Date: \n11/16/2023 \nDue Date: \n11/16/2023 \nBrainPack.io / Memetech ltd Tax ID CY10440092L Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus \nSubject: \nS00032 \nItem & Description Quantity Unit Price Sub-Total \nBrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00 Total IncludingTaxes ₪ 1.00 \nBank info Account Name : BrainPack.io / Memetech ltd Account Number: asd Bank : asd IBAN : sdas Swift (BIC) : asd ₪ 1.00 \nPlease use the following communication for your payment : INV/2023-00044'
}

class AffindaOrganization(models.Model):
    _description = 'Affinda Organization'
    _name = 'affinda.organization'

    name = fields.Char('Name')
    avatar = fields.Binary('Avatar')
    identifier = fields.Char('Identifier')
    resthookSignatureKey = fields.Char("Rest Hook Signature Key")
    workspace_ids = fields.One2many('affinda.workspace','affinda_organization',string='Workspace(s)')
    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)

    count_workspaces = fields.Integer('Workspace Count', compute='get_count_workspaces')

    uploaded_doc_count = fields.Integer('Uploaded Document Count')

    def action_show_workspaces(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "brainpack_affinda_integration.affinda_organization_action")
        action['domain'] = [('id', 'in', self.workspace_ids.ids)]
        action['context'] = {}
        return action

    @api.depends('workspace_ids')
    def get_count_workspaces(self):
        for rec in self:
            count_workspaces = 0
            if rec.workspace_ids:
                count_workspaces = len(rec.workspace_ids)
            rec.count_workspaces = count_workspaces

    def action_delete_organization(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key and self.identifier:
                url = self.company_id.affinda_api_url + "/organizations/" + self.identifier
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
                        'resthookSignatureKey': False,
                    })
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))
        else:
            raise UserError(
                ("Please check Your credentails!."))

    def action_create_organization(self):
        if self.company_id.affinda_integration:
            if self.company_id.affinda_api_url and self.company_id.affinda_api_key:
                url = self.company_id.affinda_api_url + "/organizations"

                payload = {
                    'name': self.name,
                }
                files ={}
                if self.avatar:
                    payload.update(
                        {
                            "avatar": self.avatar.decode('utf-8'),
                        }
                    )
                headers = {
                    "Authorization": "Bearer " + self.company_id.affinda_api_key,
                    "Content-Type": "application/json",
                }
                try:
                    response = requests.request("POST", url, headers=headers, json=payload)
                except requests.exceptions.ConnectionError:
                    raise UserError(
                        ("please check your internet connection."))

                if response.status_code == 201:
                    dict = json.loads(response.text)

                    self.write({
                        'identifier':dict.get('identifier'),
                        'resthookSignatureKey':dict.get('resthookSignatureKey',False),
                    })
                    # self.identifier = dict.get('identifier')
                else:
                    dict = json.loads(response.text)
                    error_msg = ",".join(
                        [error.get('code') + "\n" + error.get('detail') + "\n" for error in dict.get('errors')])
                    raise UserError(_(error_msg))
        else:
            raise UserError(
                ("Please check Your credentails!."))