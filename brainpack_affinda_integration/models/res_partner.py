from odoo import api, SUPERUSER_ID, fields, models, modules, tools, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    count_bills = fields.Integer('Bills count', compute='get_bill_count')
    bill_ids = fields.Many2many('account.move', compute='get_bill_count')

    count_receipts = fields.Integer('Receipts count', compute='get_receipts_count')
    receipts_ids = fields.Many2many('account.move', compute='get_receipts_count')

    count_credit = fields.Integer('Credits count', compute='get_credit_count')
    credit_ids = fields.Many2many('account.move', compute='get_credit_count')

    @api.depends()
    def get_credit_count(self):
        for rec in self:
            credits = self.env['account.move'].sudo().search(
                [('partner_id', '=', rec.id), ('move_type', '=', 'in_refund'),('affinda_move','=',True)]).ids
            rec.credit_ids = credits
            rec.count_credit = len(credits)

    @api.depends()
    def get_receipts_count(self):
        for rec in self:
            receipts = self.env['account.move'].sudo().search(
                [('partner_id', '=', rec.id), ('move_type', '=', 'in_receipt'),('affinda_move','=',True)]).ids
            rec.receipts_ids = receipts
            rec.count_receipts = len(receipts)

    @api.depends()
    def get_bill_count(self):
        for rec in self:
            bill_ids = self.env['account.move'].sudo().search([('partner_id', '=', rec.id),('move_type','=','in_invoice'),('affinda_move','=',True)]).ids
            rec.bill_ids = bill_ids
            rec.count_bills = len(bill_ids)

    def open_credit_move(self):
        credits = self.mapped('credit_ids')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_in_refund_type')
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
            'default_move_type': 'in_refund',
        }
        action['context'] = context
        return action

    def open_receipt_move(self):
        receipts = self.mapped('receipts_ids')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_in_receipt_type')
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
            'default_move_type': 'in_receipt',
        }
        action['context'] = context
        return action

    def open_bill_move(self):
        invoices = self.mapped('bill_ids')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_in_invoice_type')
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
            'default_move_type': 'in_invoice',
        }
        action['context'] = context
        return action