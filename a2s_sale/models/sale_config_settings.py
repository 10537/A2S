# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    journal_quick_payment = fields.Many2one(
        'account.journal', string='Journal for Quickpayments')

    @api.multi
    def set_journal_quick_payment_defaults(self):
        return self.env['ir.values'].sudo().set_default(
            'sale.config.settings', 'journal_quick_payment',
            self.journal_quick_payment.id)
