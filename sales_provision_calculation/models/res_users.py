# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import fields, models, api


class Users(models.Model):
    _inherit = "res.users"

    sales_provision_percentage = fields.Float(string='Sales Provision-%')
