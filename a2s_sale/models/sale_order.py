# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = "Sales Order Line customization for A2"
    _order = 'service_date desc'

    quick_payment = fields.Boolean(string="Quick Payment", default=True)
    service_date = fields.Date('Service date', default=fields.Date.today())
    employee_id = fields.Many2one('hr.employee', string="Employee")
    money_withheld = fields.Float(string="Money Withheld", default=0.0)
    money_release = fields.Float(string="Money Release", default=0.0)
    money_owner = fields.Many2one('res.partner', string="Customer")
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
    @api.depends('money_withheld', 'money_release', 'quick_payment')
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
