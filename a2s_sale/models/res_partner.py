# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains("vat")
    def check_vat(self):
        return False
