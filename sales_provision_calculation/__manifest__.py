# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

{
    "name": "Sales Provision Calculation",
    "version": '14.0.0.9',
    "category": 'Sales',
    "summary": """
                Sales Provision Calculation
                """,
    "sequence": 1,
    "author": "Technaureus Info Solutions Pvt. Ltd.",
    "website": "http://www.technaureus.com/",
    'currency': 'EUR',
    'license': 'Other proprietary',
    "depends": ['sale_management'],
    "data": [
        'views/res_users_views.xml',
        'views/account_move_views.xml',
    ],
    'qweb': [],
    'images': [''],
    "installable": True,
    "application": True,
    "auto_install": False,
}
