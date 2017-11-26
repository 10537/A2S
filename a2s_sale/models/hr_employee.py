# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee customization for A2"

    type_of_employee = fields.Selection(selection=[('external', 'External'), ('internal', 'Internal')],
                                        default='internal')
