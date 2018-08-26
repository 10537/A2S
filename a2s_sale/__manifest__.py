# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales A2',
    'version': '1.1',
    'category': 'Sales',
    'sequence': 35,
    'author': 'PinkDolphin SAS',
    'summary': 'Sales Workflow for A2 Company',
    'description': """
Sales Workflow 
==============
Adds new files to the SO for support the sale process on A2 company,
this module add the following fields:

On Sale Order Line:
* Employee
* Money Withheld (When the courier get the money for a delivered or
for a product payment)
* Money Release (When the courier delivery the money in A2 company)
* Owner (Is the owner of the money that the courier receives)
 
""",
    'website': 'https://www.pinkdolphin.com.co',
    'depends': ['sale', 'hr', 'product', 'account', 'base_vat'],
    'data': [
        'views/hr.xml',
        'views/product.xml',
        'views/partner.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'views/report_invoice.xml',
        'views/sale_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
