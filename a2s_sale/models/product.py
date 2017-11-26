# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Customization of product template for A2'

    external_earnings = fields.Float(string="External earnings")
    internal_earnings = fields.Float(string="Internal earnings")
