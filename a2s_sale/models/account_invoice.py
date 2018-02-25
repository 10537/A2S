# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from datetime import datetime
from odoo.tools import float_is_zero
import json


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('payment_move_line_ids.amount_residual')
    def _get_payment_info_report(self):
        lst_payment = []
        if self.payment_move_line_ids:
            info = {'title': _('Less Payment'), 'outstanding': False, 'content': []}
            currency_id = self.currency_id
            for payment in self.payment_move_line_ids:
                payment_currency_id = False
                if self.type in ('out_invoice', 'in_refund'):
                    amount = sum([p.amount for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
                    amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
                    if payment.matched_debit_ids:
                        payment_currency_id = all([p.currency_id == payment.matched_debit_ids[0].currency_id for p in payment.matched_debit_ids]) and payment.matched_debit_ids[0].currency_id or False
                elif self.type in ('in_invoice', 'out_refund'):
                    amount = sum([p.amount for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
                    amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
                    if payment.matched_credit_ids:
                        payment_currency_id = all([p.currency_id == payment.matched_credit_ids[0].currency_id for p in payment.matched_credit_ids]) and payment.matched_credit_ids[0].currency_id or False
                # get the payment value in invoice currency
                if payment_currency_id and payment_currency_id == self.currency_id:
                    amount_to_show = amount_currency
                else:
                    amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(amount, self.currency_id)
                if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
                    continue
                payment_ref = payment.move_id.name
                if payment.move_id.ref:
                    payment_ref += ' (' + payment.move_id.ref + ')'
                lst_payment.append({
                    'name': payment.name,
                    'journal_name': payment.journal_id.name,
                    'amount': amount_to_show,
                    'currency': currency_id.symbol,
                    'digits': [69, currency_id.decimal_places],
                    'date': payment.date,
                    'ref': payment_ref,
                })

        paystr = ""
        for element in lst_payment:
            paystr = paystr + _("%s Pago con ref %s - %s via" \
                                " %s por %s %s\n" % (element['date'],
                                                    element['ref'],
                                                    element['name'],
                                                    element['journal_name'],
                                                    element['amount'],
                                                    element['currency']))
        return paystr


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    quick_payment = fields.Boolean(string="Quick Payment", default=True)
    service_date = fields.Date(
        'Service date', default=lambda *a: datetime.now().strftime('%Y-%m-%d'))
    employee_id = fields.Many2one('hr.employee', string="Employee")
    money_withheld = fields.Float(string="Money Withheld", default=0.0)
    money_release = fields.Float(string="Money Release", default=0.0)
    money_owner = fields.Many2one('res.partner', string="Money Owner")
    client_earnings = fields.Float(string="Client Earnings",
                                   compute='_earnings', store=True)
    courier_earnings = fields.Float(string="Courier Earnings",
                                    compute='_earnings', store=True)
    own_earnings = fields.Float(string="My Earnings",
                                compute='_earnings', store=True)
    line_state = fields.Selection(selection=[('liquidated', 'Liquidated'),
                                             ('pending', 'Pending'),
                                             ('delivering', 'Delivering')],
                                  string="State", default='delivering')

    @api.multi
    @api.depends('money_withheld', 'money_release', 'quick_payment',
                 'discount', 'product_id')
    def _earnings(self):
        """
        Update the compute field own_earnings checking if the money have a
        owner different to the Odoo Company

        :return: Update field own_earnings
        """
        for record in self:
            courier_earnings = 0.0
            type_earning = {'internal': record.product_id.internal_earnings,
                            'external': record.product_id.external_earnings}

            if record.employee_id:
                courier_earnings = \
                    type_earning[record.employee_id.type_of_employee] or 0.0
                record.courier_earnings = courier_earnings\
                    if courier_earnings > 0.00 else 0.00

            if record.money_owner:
                if not record.quick_payment:
                    record.client_earnings = record.money_withheld or 0.00
                else:
                    money = (record.money_withheld - record.price_subtotal) \
                            or 0.00
                    record.client_earnings = money if money > 0.00 else 0.00
            amount = (record.price_subtotal - courier_earnings) or 0.00
            record.own_earnings = amount
