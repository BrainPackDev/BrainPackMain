# -*- coding: utf-8 -*-

from . import controllers
from . import wizard
from . import report
from . import models
from odoo import api, SUPERUSER_ID


def _load_account_details_post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for record in env['account.financial.report'].search(
            [('type', '=', 'account_type')]):
        if record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.account_financial_report_other_income0':
            for rec in env['account.account'].search(
                    [('account_type', '=', 'income_other')]):
                record.write({"account_ids": [(4, rec.id)]})
        elif record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.financial_report_cost_of_revenue':
            for rec in env['account.account'].search(
                    [('account_type', '=', 'expense_direct_cost')]):
                record.write({"account_ids": [(4, rec.id)]})
        elif record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.account_financial_report_operating_income0':
            for rec in env['account.account'].search(
                    [('account_type', 'in', ('equity_unaffected', 'income'))]):
                record.write({"account_ids": [(4, rec.id)]})
        elif record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.account_financial_report_expense0':
            for rec in env['account.account'].search(
                    [('account_type', 'in',
                      ('expense', 'expense_depreciation'))]):
                record.write({"account_ids": [(4, rec.id)]})
        elif record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.account_financial_report_assets0':
            for rec in env['account.account'].search(
                    [('account_type', 'in', (
                            'asset_receivable', 'asset_non_current',
                            'asset_current',
                            'asset_prepayments', 'asset_fixed',
                            'asset_cash'))]):
                record.write({"account_ids": [(4, rec.id)]})
        elif record.get_metadata()[0].get(
                'xmlid') == 'base_accounting_kit.account_financial_report_liability0':
            for rec in env['account.account'].search(
                    [('account_type', 'in', (
                            'liability_payable', 'equity',
                            'liability_current',
                            'liability_non_current',
                            'liability_credit_card'))]):
                record.write({"account_ids": [(4, rec.id)]})


def unlink_records_financial_report(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for record in env['account.financial.report'].search(
            [('type', '=', 'account_type')]):
        record.write({"account_ids": [(5, 0, 0)]})
