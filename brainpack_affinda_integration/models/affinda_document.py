from odoo import _, api, fields, models, modules, tools
import requests
from odoo.exceptions import UserError
import json
import ast
import re
from odoo.exceptions import UserError, ValidationError

# test_dict = {}
# test_dict = {
#   'bankAccountNumber': None,
#   'bankBsb': None,
#   'bankIban': None,
#   'bankSortCode': None,
#   'bankSwift': None,
#   'bpayBillerCode': None,
#   'bpayReference': None,
#   'currencyCode': {
#     'id': 91892883,
#     'rectangle': None,
#     'rectangles': [
#
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'ILS',
#     'parsed': {
#       'id': 69,
#       'label': 'ILS',
#       'value': 'ILS',
#       'synonyms': None,
#       'collection': None,
#       'description': None,
#       'organization': None
#     },
#     'confidence': None,
#     'classificationConfidence': None,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'JZguvEaB',
#     'contentType': 'enum',
#     'parent': None
#   },
#   'customerBillingAddress': {
#     'id': 91892841,
#     'rectangle': {
#       'x0': 28.938334,
#       'y0': 220.9361,
#       'x1': 120.91979,
#       'y1': 257.16968,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 28.938334,
#         'y0': 220.9361,
#         'x1': 120.91979,
#         'y1': 257.16968,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'Tes city Tarapacá 123213 Chile',
#     'parsed': {
#       'formatted': None,
#       'streetNumber': None,
#       'street': None,
#       'apartmentNumber': None,
#       'city': None,
#       'postalCode': None,
#       'state': None,
#       'country': None,
#       'rawInput': 'Tes city Tarapacá 123213 Chile',
#       'countryCode': None,
#       'latitude': None,
#       'longitude': None
#     },
#     'confidence': 0.964,
#     'classificationConfidence': 0.964,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'IIrmUFpr',
#     'contentType': 'location',
#     'parent': None
#   },
#   'customerBusinessNumber': {
#     'id': 91892842,
#     'rectangle': {
#       'x0': 59.500137,
#       'y0': 206.29315,
#       'x1': 97.49604,
#       'y1': 213.50299,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 59.500137,
#         'y0': 206.29315,
#         'x1': 97.49604,
#         'y1': 213.50299,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '1234567',
#     'parsed': '1234567',
#     'confidence': 0.902,
#     'classificationConfidence': 0.902,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'sQTrimjN',
#     'contentType': 'text',
#     'parent': None
#   },
#   'customerCompanyName': {
#     'id': 91892843,
#     'rectangle': {
#       'x0': 29.732218,
#       'y0': 188.82288,
#       'x1': 173.61119,
#       'y1': 200.38727,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 29.732218,
#         'y0': 188.82288,
#         'x1': 173.61119,
#         'y1': 200.38727,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'Etamar Company, Etamar',
#     'parsed': 'Etamar Company, Etamar',
#     'confidence': 0.969,
#     'classificationConfidence': 0.969,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'YCquITSP',
#     'contentType': 'text',
#     'parent': None
#   },
#   'customerContactName': None,
#   'customerDeliveryAddress': None,
#   'customerEmail': None,
#   'customerNumber': None,
#   'customerPhoneNumber': None,
#   'customerVat': None,
#   'invoiceDate': {
#     'id': 91892844,
#     'rectangle': {
#       'x0': 293.07248,
#       'y0': 188.67004,
#       'x1': 360.4007,
#       'y1': 198.85895,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 293.07248,
#         'y0': 188.67004,
#         'x1': 360.4007,
#         'y1': 198.85895,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '11/16/2023',
#     'parsed': '2023-11-16',
#     'confidence': 0.976,
#     'classificationConfidence': 0.976,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'sRakysMP',
#     'contentType': 'date',
#     'parent': None
#   },
#   'invoiceNumber': {
#     'id': 91892845,
#     'rectangle': {
#       'x0': 199.86053,
#       'y0': 80.26367,
#       'x1': 283.4602,
#       'y1': 91.620056,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 199.86053,
#         'y0': 80.26367,
#         'x1': 283.4602,
#         'y1': 91.620056,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '2023-00044',
#     'parsed': '2023-00044',
#     'confidence': 0.976,
#     'classificationConfidence': 0.976,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'bWFyBeNU',
#     'contentType': 'text',
#     'parent': None
#   },
#   'invoiceOrderDate': None,
#   'invoicePurchaseOrderNumber': None,
#   'openingBalance': None,
#   'paymentAmountBase': None,
#   'paymentAmountDue': {
#     'id': 91892846,
#     'rectangle': {
#       'x0': 495.408,
#       'y0': 446.34213,
#       'x1': 558.7743,
#       'y1': 462.36838,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 495.408,
#         'y0': 446.34213,
#         'x1': 558.7743,
#         'y1': 462.36838,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '₪ 1.00',
#     'parsed': '1.00',
#     'confidence': 0.676,
#     'classificationConfidence': 0.676,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'hTyimjpc',
#     'contentType': 'decimal',
#     'parent': None
#   },
#   'paymentAmountPaid': None,
#   'paymentAmountTax': None,
#   'paymentAmountTotal': {
#     'id': 91892847,
#     'rectangle': {
#       'x0': 533.8134,
#       'y0': 338.91608,
#       'x1': 559.73895,
#       'y1': 345.76627,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 533.8134,
#         'y0': 338.91608,
#         'x1': 559.73895,
#         'y1': 345.76627,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '₪ 1.00',
#     'parsed': '1.00',
#     'confidence': 0.659,
#     'classificationConfidence': 0.659,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'jeMSNwCq',
#     'contentType': 'decimal',
#     'parent': None
#   },
#   'paymentDateDue': {
#     'id': 91892848,
#     'rectangle': {
#       'x0': 293.07248,
#       'y0': 231.73022,
#       'x1': 360.4007,
#       'y1': 241.91913,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 293.07248,
#         'y0': 231.73022,
#         'x1': 360.4007,
#         'y1': 241.91913,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': '11/16/2023',
#     'parsed': '2023-11-16',
#     'confidence': 0.974,
#     'classificationConfidence': 0.974,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'RmsWpucw',
#     'contentType': 'date',
#     'parent': None
#   },
#   'paymentDelivery': None,
#   'paymentOtherCharges': None,
#   'paymentReference': {
#     'id': 91892849,
#     'rectangle': {
#       'x0': 279.5364,
#       'y0': 518.45636,
#       'x1': 353.57785,
#       'y1': 526.21936,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 279.5364,
#         'y0': 518.45636,
#         'x1': 353.57785,
#         'y1': 526.21936,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'INV/2023-00044',
#     'parsed': 'INV/2023-00044',
#     'confidence': 0.589,
#     'classificationConfidence': 0.589,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'CZQkkTuw',
#     'contentType': 'text',
#     'parent': None
#   },
#   'paymentTerms': None,
#   'supplierAddress': {
#     'id': 91892850,
#     'rectangle': {
#       'x0': 495.23514,
#       'y0': 88.51062,
#       'x1': 565.8834,
#       'y1': 126.529785,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 495.23514,
#         'y0': 88.51062,
#         'x1': 565.8834,
#         'y1': 126.529785,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus',
#     'parsed': {
#       'formatted': None,
#       'streetNumber': None,
#       'street': None,
#       'apartmentNumber': None,
#       'city': None,
#       'postalCode': None,
#       'state': None,
#       'country': None,
#       'rawInput': 'Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus',
#       'countryCode': None,
#       'latitude': None,
#       'longitude': None
#     },
#     'confidence': 0.979,
#     'classificationConfidence': 0.979,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'HRTaEvcW',
#     'contentType': 'location',
#     'parent': None
#   },
#   'supplierBusinessNumber': {
#     'id': 91892851,
#     'rectangle': {
#       'x0': 502.2946,
#       'y0': 74.06183,
#       'x1': 564.35254,
#       'y1': 81.27167,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 502.2946,
#         'y0': 74.06183,
#         'x1': 564.35254,
#         'y1': 81.27167,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'CY10440092L',
#     'parsed': 'CY10440092L',
#     'confidence': 0.924,
#     'classificationConfidence': 0.924,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'rvshbPQZ',
#     'contentType': 'text',
#     'parent': None
#   },
#   'supplierCompanyName': {
#     'id': 91892852,
#     'rectangle': {
#       'x0': 445.0864,
#       'y0': 59.38983,
#       'x1': 563.24133,
#       'y1': 67.075134,
#       'pageIndex': 0
#     },
#     'rectangles': [
#       {
#         'x0': 445.0864,
#         'y0': 59.38983,
#         'x1': 563.24133,
#         'y1': 67.075134,
#         'pageIndex': 0
#       }
#     ],
#     'document': 'zJlGVIfW',
#     'pageIndex': 0,
#     'raw': 'BrainPack.io / Memetech ltd',
#     'parsed': 'BrainPack.io / Memetech ltd',
#     'confidence': 0.973,
#     'classificationConfidence': 0.973,
#     'textExtractionConfidence': 1.0,
#     'isVerified': False,
#     'isClientVerified': False,
#     'isAutoVerified': False,
#     'dataPoint': 'rFeFJcwy',
#     'contentType': 'text',
#     'parent': None
#   },
#   'supplierEmail': None,
#   'supplierFax': None,
#   'supplierPhoneNumber': None,
#   'supplierVat': None,
#   'supplierWebsite': None,
#   'tables': None,
#   'tablesBeta': [
#     {
#       'id': 91892853,
#       'rectangle': {
#         'x0': 30.501642223196722,
#         'y0': 300.4959,
#         'x1': 565.1140097768033,
#         'y1': 319.1043097768033,
#         'pageIndex': 0
#       },
#       'rectangles': [
#         {
#           'x0': 30.501642223196722,
#           'y0': 300.4959,
#           'x1': 565.1140097768033,
#           'y1': 319.1043097768033,
#           'pageIndex': 0
#         }
#       ],
#       'document': 'zJlGVIfW',
#       'pageIndex': 0,
#       'raw': None,
#       'parsed': {
#         'rows': [
#           {
#             'id': 91892869,
#             'rectangle': {
#               'x0': 30.501642223196722,
#               'y0': 300.4959,
#               'x1': 565.1140097768033,
#               'y1': 319.1043097768033,
#               'pageIndex': 0
#             },
#             'rectangles': [
#               {
#                 'x0': 30.501642223196722,
#                 'y0': 300.4959,
#                 'x1': 565.1140097768033,
#                 'y1': 319.1043097768033,
#                 'pageIndex': 0
#               }
#             ],
#             'document': 'zJlGVIfW',
#             'pageIndex': 0,
#             'raw': 'BrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00',
#             'parsed': {
#               'itemDescriptionBeta': {
#                 'id': 91892871,
#                 'rectangle': {
#                   'x0': 35.658752,
#                   'y0': 305.4959,
#                   'x1': 193.48831,
#                   'y1': 313.9472,
#                   'pageIndex': 0
#                 },
#                 'rectangles': [
#                   {
#                     'x0': 35.658752,
#                     'y0': 305.4959,
#                     'x1': 193.48831,
#                     'y1': 313.9472,
#                     'pageIndex': 0
#                   }
#                 ],
#                 'document': 'zJlGVIfW',
#                 'pageIndex': 0,
#                 'raw': 'BrainPack Licensing - Base Cloud Server',
#                 'parsed': 'BrainPack Licensing - Base Cloud Server',
#                 'confidence': 0.998,
#                 'classificationConfidence': 0.998,
#                 'textExtractionConfidence': 1.0,
#                 'isVerified': False,
#                 'isClientVerified': False,
#                 'isAutoVerified': False,
#                 'dataPoint': 'arJqZwjI',
#                 'contentType': 'text',
#                 'parent': 91892869
#               },
#               'itemTotalBeta': {
#                 'id': 91892873,
#                 'rectangle': {
#                   'x0': 533.8134,
#                   'y0': 305.55957,
#                   'x1': 559.9569,
#                   'y1': 312.4098,
#                   'pageIndex': 0
#                 },
#                 'rectangles': [
#                   {
#                     'x0': 533.8134,
#                     'y0': 305.55957,
#                     'x1': 559.9569,
#                     'y1': 312.4098,
#                     'pageIndex': 0
#                   }
#                 ],
#                 'document': 'zJlGVIfW',
#                 'pageIndex': 0,
#                 'raw': '₪ 1.00',
#                 'parsed': '1.00',
#                 'confidence': 0.878,
#                 'classificationConfidence': 0.878,
#                 'textExtractionConfidence': 1.0,
#                 'isVerified': False,
#                 'isClientVerified': False,
#                 'isAutoVerified': False,
#                 'dataPoint': 'KVMQbSOq',
#                 'contentType': 'decimal',
#                 'parent': 91892869
#               },
#               'itemUnitBeta': {
#                 'id': 91892872,
#                 'rectangle': {
#                   'x0': 361.88202,
#                   'y0': 305.55957,
#                   'x1': 382.10928,
#                   'y1': 312.35516,
#                   'pageIndex': 0
#                 },
#                 'rectangles': [
#                   {
#                     'x0': 361.88202,
#                     'y0': 305.55957,
#                     'x1': 382.10928,
#                     'y1': 312.35516,
#                     'pageIndex': 0
#                   }
#                 ],
#                 'document': 'zJlGVIfW',
#                 'pageIndex': 0,
#                 'raw': 'Units',
#                 'parsed': 'Units',
#                 'confidence': 0.707,
#                 'classificationConfidence': 0.707,
#                 'textExtractionConfidence': 1.0,
#                 'isVerified': False,
#                 'isClientVerified': False,
#                 'isAutoVerified': False,
#                 'dataPoint': 'xuRjCxVR',
#                 'contentType': 'text',
#                 'parent': 91892869
#               },
#               'itemQuantityBeta': {
#                 'id': 91892874,
#                 'rectangle': {
#                   'x0': 342.66565,
#                   'y0': 305.59595,
#                   'x1': 359.2116,
#                   'y1': 312.35516,
#                   'pageIndex': 0
#                 },
#                 'rectangles': [
#                   {
#                     'x0': 342.66565,
#                     'y0': 305.59595,
#                     'x1': 359.2116,
#                     'y1': 312.35516,
#                     'pageIndex': 0
#                   }
#                 ],
#                 'document': 'zJlGVIfW',
#                 'pageIndex': 0,
#                 'raw': '1.00',
#                 'parsed': 1.0,
#                 'confidence': 0.997,
#                 'classificationConfidence': 0.997,
#                 'textExtractionConfidence': 1.0,
#                 'isVerified': False,
#                 'isClientVerified': False,
#                 'isAutoVerified': False,
#                 'dataPoint': 'LoylITwn',
#                 'contentType': 'float',
#                 'parent': 91892869
#               },
#               'itemUnitPriceBeta': {
#                 'id': 91892870,
#                 'rectangle': {
#                   'x0': 454.2582,
#                   'y0': 305.59595,
#                   'x1': 470.80417,
#                   'y1': 312.35516,
#                   'pageIndex': 0
#                 },
#                 'rectangles': [
#                   {
#                     'x0': 454.2582,
#                     'y0': 305.59595,
#                     'x1': 470.80417,
#                     'y1': 312.35516,
#                     'pageIndex': 0
#                   }
#                 ],
#                 'document': 'zJlGVIfW',
#                 'pageIndex': 0,
#                 'raw': '1.00',
#                 'parsed': '1.00',
#                 'confidence': 0.997,
#                 'classificationConfidence': 0.997,
#                 'textExtractionConfidence': 1.0,
#                 'isVerified': False,
#                 'isClientVerified': False,
#                 'isAutoVerified': False,
#                 'dataPoint': 'EJQqPpQh',
#                 'contentType': 'decimal',
#                 'parent': 91892869
#               }
#             },
#             'confidence': None,
#             'classificationConfidence': None,
#             'textExtractionConfidence': 1.0,
#             'isVerified': False,
#             'isClientVerified': False,
#             'isAutoVerified': False,
#             'dataPoint': 'kCodJrel',
#             'contentType': 'group',
#             'parent': 91892853
#           }
#         ]
#       },
#       'confidence': None,
#       'classificationConfidence': None,
#       'textExtractionConfidence': 1.0,
#       'isVerified': False,
#       'isClientVerified': False,
#       'isAutoVerified': False,
#       'dataPoint': 'ftkJQmWB',
#       'contentType': 'table',
#       'parent': None
#     }
#   ],
#   'rawText': 'Client Name \nEtamar Company, Etamar \nTax ID 1234567 Tes city Tarapacá 123213 Chile \nINVOICE \n# 2023-00044 \nInvoice Date: \n11/16/2023 \nDue Date: \n11/16/2023 \nBrainPack.io / Memetech ltd Tax ID CY10440092L Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus \nSubject: \nS00032 \nItem & Description Quantity Unit Price Sub-Total \nBrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00 Total IncludingTaxes ₪ 1.00 \nBank info Account Name : BrainPack.io / Memetech ltd Account Number: asd Bank : asd IBAN : sdas Swift (BIC) : asd ₪ 1.00 \nPlease use the following communication for your payment : INV/2023-00044'
# }

test_dict =  {
            "bankAccountNumber": None,
            "bankBsb": None,
            "bankIban": None,
            "bankSortCode": None,
            "bankSwift": None,
            "bpayBillerCode": None,
            "bpayReference": None,
            "currencyCode": {
                "id": 91892883,
                "rectangle": None,
                "rectangles": [
                    
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "ILS",
                "parsed": {
                    "id": 69,
                    "label": "ILS",
                    "value": "ILS",
                    "synonyms": None,
                    "collection": None,
                    "description": None,
                    "organization": None
                },
                "confidence": None,
                "classificationConfidence": None,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "JZguvEaB",
                "contentType": "enum",
                "parent": None
            },
            "customerBillingAddress": {
                "id": 91892841,
                "rectangle": {
                    "x0": 28.938334,
                    "y0": 220.9361,
                    "x1": 120.91979,
                    "y1": 257.16968,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 28.938334,
                        "y0": 220.9361,
                        "x1": 120.91979,
                        "y1": 257.16968,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "Tes city Tarapacá 123213 Chile",
                "parsed": {
                    "formatted": None,
                    "streetNumber": None,
                    "street": None,
                    "apartmentNumber": None,
                    "city": None,
                    "postalCode": None,
                    "state": None,
                    "country": None,
                    "rawInput": "Tes city Tarapacá 123213 Chile",
                    "countryCode": None,
                    "latitude": None,
                    "longitude": None
                },
                "confidence": 0.964,
                "classificationConfidence": 0.964,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "IIrmUFpr",
                "contentType": "location",
                "parent": None
            },
            "customerBusinessNumber": {
                "id": 91892842,
                "rectangle": {
                    "x0": 59.500137,
                    "y0": 206.29315,
                    "x1": 97.49604,
                    "y1": 213.50299,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 59.500137,
                        "y0": 206.29315,
                        "x1": 97.49604,
                        "y1": 213.50299,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "1234567",
                "parsed": "1234567",
                "confidence": 0.902,
                "classificationConfidence": 0.902,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "sQTrimjN",
                "contentType": "text",
                "parent": None
            },
            "customerCompanyName": None,
            "customerContactName": {
                "id": 92807947,
                "rectangle": {
                    "x0": 131.24352331606218,
                    "y0": 187.27250647668396,
                    "x1": 177.04663212435233,
                    "y1": 201.80618523316062,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 131.24352331606218,
                        "y0": 187.27250647668396,
                        "x1": 177.04663212435233,
                        "y1": 201.80618523316062,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "Etamar",
                "parsed": "Etamar",
                "confidence": None,
                "classificationConfidence": None,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "lmWEjOYu",
                "contentType": "text",
                "parent": None
            },
            "customerDeliveryAddress": None,
            "customerEmail": {
                "id": 92045419,
                "rectangle": {
                    "x0": 59.4559585492228,
                    "y0": 205.3295012953368,
                    "x1": 98.65284974093265,
                    "y1": 212.81654792746116,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 59.4559585492228,
                        "y0": 205.3295012953368,
                        "x1": 98.65284974093265,
                        "y1": 212.81654792746116,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "1234567",
                "parsed": "1234567",
                "confidence": None,
                "classificationConfidence": None,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "GIpfNtwK",
                "contentType": "text",
                "parent": None
            },
            "customerNumber": None,
            "customerPhoneNumber": {
                "id": 92768173,
                "rectangle": {
                    "x0": 59.01554404145078,
                    "y0": 205.7699158031088,
                    "x1": 97.7720207253886,
                    "y1": 215.8994494818653,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 59.01554404145078,
                        "y0": 205.7699158031088,
                        "x1": 97.7720207253886,
                        "y1": 215.8994494818653,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "1234567",
                "parsed": "1234567",
                "confidence": None,
                "classificationConfidence": None,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "GVFfAmte",
                "contentType": "text",
                "parent": None
            },
            "customerVat": {
                "id": 92769882,
                "rectangle": {
                    "x0": 59.01554404145078,
                    "y0": 205.3295012953368,
                    "x1": 101.7357512953368,
                    "y1": 214.1377914507772,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 59.01554404145078,
                        "y0": 205.3295012953368,
                        "x1": 101.7357512953368,
                        "y1": 214.1377914507772,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "1234567",
                "parsed": "1234567",
                "confidence": None,
                "classificationConfidence": None,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "KfVWujnA",
                "contentType": "text",
                "parent": None
            },
            "invoiceDate": {
                "id": 91892844,
                "rectangle": {
                    "x0": 293.07248,
                    "y0": 188.67004,
                    "x1": 360.4007,
                    "y1": 198.85895,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 293.07248,
                        "y0": 188.67004,
                        "x1": 360.4007,
                        "y1": 198.85895,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "11/16/2023",
                "parsed": "2023-11-16",
                "confidence": 0.976,
                "classificationConfidence": 0.976,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "sRakysMP",
                "contentType": "date",
                "parent": None
            },
            "invoiceNumber": {
                "id": 91892845,
                "rectangle": {
                    "x0": 199.86053,
                    "y0": 80.26367,
                    "x1": 283.4602,
                    "y1": 91.620056,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 199.86053,
                        "y0": 80.26367,
                        "x1": 283.4602,
                        "y1": 91.620056,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "2023-00044",
                "parsed": "2023-00044",
                "confidence": 0.976,
                "classificationConfidence": 0.976,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "bWFyBeNU",
                "contentType": "text",
                "parent": None
            },
            "invoiceOrderDate": None,
            "invoicePurchaseOrderNumber": None,
            "openingBalance": None,
            "paymentAmountBase": None,
            "paymentAmountDue": {
                "id": 91892846,
                "rectangle": {
                    "x0": 495.408,
                    "y0": 446.34213,
                    "x1": 558.7743,
                    "y1": 462.36838,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 495.408,
                        "y0": 446.34213,
                        "x1": 558.7743,
                        "y1": 462.36838,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "₪ 1.00",
                "parsed": "1.00",
                "confidence": 0.676,
                "classificationConfidence": 0.676,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "hTyimjpc",
                "contentType": "decimal",
                "parent": None
            },
            "paymentAmountPaid": None,
            "paymentAmountTax": None,
            "paymentAmountTotal": {
                "id": 91892847,
                "rectangle": {
                    "x0": 533.8134,
                    "y0": 338.91608,
                    "x1": 559.73895,
                    "y1": 345.76627,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 533.8134,
                        "y0": 338.91608,
                        "x1": 559.73895,
                        "y1": 345.76627,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "₪ 1.00",
                "parsed": "1.00",
                "confidence": 0.659,
                "classificationConfidence": 0.659,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "jeMSNwCq",
                "contentType": "decimal",
                "parent": None
            },
            "paymentDateDue": {
                "id": 91892848,
                "rectangle": {
                    "x0": 293.07248,
                    "y0": 231.73022,
                    "x1": 360.4007,
                    "y1": 241.91913,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 293.07248,
                        "y0": 231.73022,
                        "x1": 360.4007,
                        "y1": 241.91913,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "11/16/2023",
                "parsed": "2023-11-16",
                "confidence": 0.974,
                "classificationConfidence": 0.974,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "RmsWpucw",
                "contentType": "date",
                "parent": None
            },
            "paymentDelivery": None,
            "paymentOtherCharges": None,
            "paymentReference": {
                "id": 91892849,
                "rectangle": {
                    "x0": 279.5364,
                    "y0": 518.45636,
                    "x1": 353.57785,
                    "y1": 526.21936,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 279.5364,
                        "y0": 518.45636,
                        "x1": 353.57785,
                        "y1": 526.21936,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "INV/2023-00044",
                "parsed": "INV/2023-00044",
                "confidence": 0.589,
                "classificationConfidence": 0.589,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "CZQkkTuw",
                "contentType": "text",
                "parent": None
            },
            "paymentTerms": None,
            "supplierAddress": {
                "id": 91892850,
                "rectangle": {
                    "x0": 495.23514,
                    "y0": 88.51062,
                    "x1": 565.8834,
                    "y1": 126.529785,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 495.23514,
                        "y0": 88.51062,
                        "x1": 565.8834,
                        "y1": 126.529785,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus",
                "parsed": {
                    "formatted": None,
                    "streetNumber": None,
                    "street": None,
                    "apartmentNumber": None,
                    "city": None,
                    "postalCode": None,
                    "state": None,
                    "country": None,
                    "rawInput": "Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus",
                    "countryCode": None,
                    "latitude": None,
                    "longitude": None
                },
                "confidence": 0.979,
                "classificationConfidence": 0.979,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "HRTaEvcW",
                "contentType": "location",
                "parent": None
            },
            "supplierBusinessNumber": {
                "id": 91892851,
                "rectangle": {
                    "x0": 502.2946,
                    "y0": 74.06183,
                    "x1": 564.35254,
                    "y1": 81.27167,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 502.2946,
                        "y0": 74.06183,
                        "x1": 564.35254,
                        "y1": 81.27167,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "CY10440092L",
                "parsed": "CY10440092L",
                "confidence": 0.924,
                "classificationConfidence": 0.924,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "rvshbPQZ",
                "contentType": "text",
                "parent": None
            },
            "supplierCompanyName": {
                "id": 91892852,
                "rectangle": {
                    "x0": 445.0864,
                    "y0": 59.38983,
                    "x1": 563.24133,
                    "y1": 67.075134,
                    "pageIndex": 0
                },
                "rectangles": [
                    {
                        "x0": 445.0864,
                        "y0": 59.38983,
                        "x1": 563.24133,
                        "y1": 67.075134,
                        "pageIndex": 0
                    }
                ],
                "document": "zJlGVIfW",
                "pageIndex": 0,
                "raw": "BrainPack.io / Memetech ltd",
                "parsed": "BrainPack.io / Memetech ltd",
                "confidence": 0.973,
                "classificationConfidence": 0.973,
                "textExtractionConfidence": 1.0,
                "isVerified": False,
                "isClientVerified": False,
                "isAutoVerified": False,
                "dataPoint": "rFeFJcwy",
                "contentType": "text",
                "parent": None
            },
            "supplierEmail": None,
            "supplierFax": None,
            "supplierPhoneNumber": None,
            "supplierVat": None,
            "supplierWebsite": None,
            "tables": None,
            "tablesBeta": [
                {
                    "id": 91892853,
                    "rectangle": {
                        "x0": 30.501642223196722,
                        "y0": 300.4959,
                        "x1": 565.1140097768033,
                        "y1": 319.1043097768033,
                        "pageIndex": 0
                    },
                    "rectangles": [
                        {
                            "x0": 30.501642223196722,
                            "y0": 300.4959,
                            "x1": 565.1140097768033,
                            "y1": 319.1043097768033,
                            "pageIndex": 0
                        }
                    ],
                    "document": "zJlGVIfW",
                    "pageIndex": 0,
                    "raw": None,
                    "parsed": {
                        "rows": [
                            {
                                "id": 91892869,
                                "rectangle": {
                                    "x0": 30.501642223196722,
                                    "y0": 300.4959,
                                    "x1": 565.1140097768033,
                                    "y1": 319.1043097768033,
                                    "pageIndex": 0
                                },
                                "rectangles": [
                                    {
                                        "x0": 30.501642223196722,
                                        "y0": 300.4959,
                                        "x1": 565.1140097768033,
                                        "y1": 319.1043097768033,
                                        "pageIndex": 0
                                    }
                                ],
                                "document": "zJlGVIfW",
                                "pageIndex": 0,
                                "raw": "BrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00",
                                "parsed": {
                                    "itemDescriptionBeta": {
                                        "id": 91892871,
                                        "rectangle": {
                                            "x0": 35.658752,
                                            "y0": 305.4959,
                                            "x1": 193.48831,
                                            "y1": 313.9472,
                                            "pageIndex": 0
                                        },
                                        "rectangles": [
                                            {
                                                "x0": 35.658752,
                                                "y0": 305.4959,
                                                "x1": 193.48831,
                                                "y1": 313.9472,
                                                "pageIndex": 0
                                            }
                                        ],
                                        "document": "zJlGVIfW",
                                        "pageIndex": 0,
                                        "raw": "BrainPack Licensing - Base Cloud Server",
                                        "parsed": "BrainPack Licensing - Base Cloud Server11",
                                        "confidence": 0.998,
                                        "classificationConfidence": 0.998,
                                        "textExtractionConfidence": 1.0,
                                        "isVerified": False,
                                        "isClientVerified": False,
                                        "isAutoVerified": False,
                                        "dataPoint": "arJqZwjI",
                                        "contentType": "text",
                                        "parent": 91892869
                                    },
                                    "itemTotalBeta": {
                                        "id": 91892873,
                                        "rectangle": {
                                            "x0": 533.8134,
                                            "y0": 305.55957,
                                            "x1": 559.9569,
                                            "y1": 312.4098,
                                            "pageIndex": 0
                                        },
                                        "rectangles": [
                                            {
                                                "x0": 533.8134,
                                                "y0": 305.55957,
                                                "x1": 559.9569,
                                                "y1": 312.4098,
                                                "pageIndex": 0
                                            }
                                        ],
                                        "document": "zJlGVIfW",
                                        "pageIndex": 0,
                                        "raw": "₪ 1.00",
                                        "parsed": "1.00",
                                        "confidence": 0.878,
                                        "classificationConfidence": 0.878,
                                        "textExtractionConfidence": 1.0,
                                        "isVerified": False,
                                        "isClientVerified": False,
                                        "isAutoVerified": False,
                                        "dataPoint": "KVMQbSOq",
                                        "contentType": "decimal",
                                        "parent": 91892869
                                    },
                                    "itemUnitBeta": {
                                        "id": 91892872,
                                        "rectangle": {
                                            "x0": 361.88202,
                                            "y0": 305.55957,
                                            "x1": 382.10928,
                                            "y1": 312.35516,
                                            "pageIndex": 0
                                        },
                                        "rectangles": [
                                            {
                                                "x0": 361.88202,
                                                "y0": 305.55957,
                                                "x1": 382.10928,
                                                "y1": 312.35516,
                                                "pageIndex": 0
                                            }
                                        ],
                                        "document": "zJlGVIfW",
                                        "pageIndex": 0,
                                        "raw": "Units",
                                        "parsed": "Units",
                                        "confidence": 0.707,
                                        "classificationConfidence": 0.707,
                                        "textExtractionConfidence": 1.0,
                                        "isVerified": False,
                                        "isClientVerified": False,
                                        "isAutoVerified": False,
                                        "dataPoint": "xuRjCxVR",
                                        "contentType": "text",
                                        "parent": 91892869
                                    },
                                    "itemQuantityBeta": {
                                        "id": 91892874,
                                        "rectangle": {
                                            "x0": 342.66565,
                                            "y0": 305.59595,
                                            "x1": 359.2116,
                                            "y1": 312.35516,
                                            "pageIndex": 0
                                        },
                                        "rectangles": [
                                            {
                                                "x0": 342.66565,
                                                "y0": 305.59595,
                                                "x1": 359.2116,
                                                "y1": 312.35516,
                                                "pageIndex": 0
                                            }
                                        ],
                                        "document": "zJlGVIfW",
                                        "pageIndex": 0,
                                        "raw": "1.00",
                                        "parsed": 1.0,
                                        "confidence": 0.997,
                                        "classificationConfidence": 0.997,
                                        "textExtractionConfidence": 1.0,
                                        "isVerified": False,
                                        "isClientVerified": False,
                                        "isAutoVerified": False,
                                        "dataPoint": "LoylITwn",
                                        "contentType": "float",
                                        "parent": 91892869
                                    },
                                    "itemUnitPriceBeta": {
                                        "id": 91892870,
                                        "rectangle": {
                                            "x0": 454.2582,
                                            "y0": 305.59595,
                                            "x1": 470.80417,
                                            "y1": 312.35516,
                                            "pageIndex": 0
                                        },
                                        "rectangles": [
                                            {
                                                "x0": 454.2582,
                                                "y0": 305.59595,
                                                "x1": 470.80417,
                                                "y1": 312.35516,
                                                "pageIndex": 0
                                            }
                                        ],
                                        "document": "zJlGVIfW",
                                        "pageIndex": 0,
                                        "raw": "1.00",
                                        "parsed": "1.00",
                                        "confidence": 0.997,
                                        "classificationConfidence": 0.997,
                                        "textExtractionConfidence": 1.0,
                                        "isVerified": False,
                                        "isClientVerified": False,
                                        "isAutoVerified": False,
                                        "dataPoint": "EJQqPpQh",
                                        "contentType": "decimal",
                                        "parent": 91892869
                                    }
                                },
                                "confidence": None,
                                "classificationConfidence": None,
                                "textExtractionConfidence": 1.0,
                                "isVerified": False,
                                "isClientVerified": False,
                                "isAutoVerified": False,
                                "dataPoint": "kCodJrel",
                                "contentType": "group",
                                "parent": 91892853
                            }
                        ]
                    },
                    "confidence": None,
                    "classificationConfidence": None,
                    "textExtractionConfidence": 1.0,
                    "isVerified": False,
                    "isClientVerified": False,
                    "isAutoVerified": False,
                    "dataPoint": "ftkJQmWB",
                    "contentType": "table",
                    "parent": None
                }
            ],
            "rawText": "Client Name \nEtamar Company, Etamar \nTax ID 1234567 Tes city Tarapacá 123213 Chile \nINVOICE \n# 2023-00044 \nInvoice Date: \n11/16/2023 \nDue Date: \n11/16/2023 \nBrainPack.io / Memetech ltd Tax ID CY10440092L Agiou Pavlou 61 Agios Andreas Nicosia, Cyprus \nSubject: \nS00032 \nItem & Description Quantity Unit Price Sub-Total \nBrainPack Licensing - Base Cloud Server 1.00 Units 1.00 ₪ 1.00 Total IncludingTaxes ₪ 1.00 \nBank info Account Name : BrainPack.io / Memetech ltd Account Number: asd Bank : asd IBAN : sdas Swift (BIC) : asd ₪ 1.00 \nPlease use the following communication for your payment : INV/2023-00044"
        }
class AffindaDocument(models.Model):
    _description = 'Affinda Document'
    _name = 'affinda.document'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'file_name'

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
                                if 'itemDescriptionBeta' in parsed_dict and parsed_dict.get('itemDescriptionBeta') and 'itemQuantityBeta' in parsed_dict and parsed_dict.get('itemQuantityBeta'):
                                    product_name = parsed_dict.get('itemDescriptionBeta').get('parsed')
                                    product = self.env['product.product'].sudo().search([('name','=',product_name)])
                                    product_uom = False
                                    product_price = 1

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
                                        if '%' in parsed_dict.get('itemTaxRateBeta').get('parsed'):
                                            lst_tax = re.findall(r'\b\d+\b',
                                                                 parsed_dict.get('itemTaxRateBeta').get('parsed'))
                                            if lst_tax:
                                                tax_amount = lst_tax[0]
                                                # tax_amount = parsed_dict.get('itemTaxRateBeta').get('parsed').replace('%','')
                                                if tax_amount:
                                                    tax = self.env['account.tax'].sudo().search([('amount','=',float(tax_amount)),('type_tax_use','=','sale'),('amount_type','=','percent'),('company_id','=',self.company_id.id)])
                                                    if not tax:
                                                        tax = self.env['account.tax'].sudo().create({
                                                            'name' : 'Tax ' + parsed_dict.get('itemTaxRateBeta').get('parsed'),
                                                            'amount_type' : 'percent',
                                                            'type_tax_use' : 'sale',
                                                            'amount' : float(tax_amount),
                                                            'company_id': self.company_id.id
                                                        })
                                        else:
                                            lst_tax = re.findall(r'\b\d+\b', parsed_dict.get('itemTaxRateBeta').get('parsed'))
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
                                                                'parsed'),
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
                                        'quantity' : parsed_dict.get('itemQuantityBeta').get('parsed'),
                                    }

                                    move_lines.append(line_val)
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

