# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    _description = "Sales Order Line customization for A2"

    service_date = fields.Date('Service date', default=fields.Date.today())
    employee_id = fields.Many2one('hr.employee', string="Employee")
    money_withheld = fields.Float(string="Money Withheld", default=0.0)
    money_release = fields.Float(string="Money Release", default=0.0)
    money_owner = fields.Many2one('res.partner', string="Customer")
    client_earnings = fields.Float(string="Client Earnings", compute='_earnings', store=True)
    courier_earnings = fields.Float(string="Courier Earnings", compute='_earnings', store=True)
    own_earnings = fields.Float(string="My Earnings", compute='_earnings', store=True)
    line_state = fields.Selection(selection=[('liquidated', 'Liquidated'), ('pending', 'Pending'),
                                             ('delivering', 'Delivering')], string="State", default='delivering')

    @api.multi
    @api.depends('money_withheld', 'money_release')
    def _earnings(self):
        """
        Update the compute field own_earnings checking if the money have a owner different to the Odoo Company
        :return: Update field own_earnings
        """
        for record in self:
            courier_earnings = 0.0
            type_earning = {'internal': record.product_id.internal_earnings,
                            'external': record.product_id.external_earnings}

            if record.employee_id:
                courier_earnings = type_earning[record.employee_id.type_of_employee] or 0.0
                record.courier_earnings = courier_earnings

            if record.money_owner:
                money = (record.money_withheld - record.price_subtotal) or 0.0
                record.client_earnings = money

            record.own_earnings = (record.price_subtotal - courier_earnings) or 0.0
