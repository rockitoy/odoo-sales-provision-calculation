# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    sales_provision_percentage = fields.Float(string='Provision-%', store=True,
                                              compute='onchange_user_id_sale_provision')
    provision_amount = fields.Float(string='Provision', compute='_get_provision_amount', store=True)
    margin = fields.Float(string='Margin', compute='_get_provision_amount', store=True)

    @api.depends('invoice_user_id')
    def onchange_user_id_sale_provision(self):
        if self.invoice_user_id:
            if self.invoice_user_id.sales_provision_percentage:
                self.sales_provision_percentage = self.invoice_user_id.sales_provision_percentage
            else:
                self.sales_provision_percentage = 0
        else:
            self.sales_provision_percentage = 0

    @api.depends('amount_untaxed', 'sales_provision_percentage')
    def _get_provision_amount(self):
        for vals in self:
            if vals.invoice_line_ids:
                margin = 0.0
                for product in vals.invoice_line_ids:
                    if product.product_id.standard_price:
                        std_price = product.product_id.standard_price
                        line_margin = product.price_subtotal - (std_price * product.quantity)
                        margin += line_margin
                    else:
                        continue
                vals.margin = margin
            else:
                vals.margin = 0.0

            if vals.amount_untaxed and vals.sales_provision_percentage and vals.margin:
                vals.provision_amount = (vals.margin * vals.sales_provision_percentage) / 100
            else:
                vals.provision_amount = 0.0


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    # provision_amount = fields.Float(string='Provision', readonly=True)
    # margin = fields.Float(string='Margin', readonly=True)
    line_margin = fields.Float("Margin", readonly=True)
    line_provision_amount = fields.Float(string='Provision')

    @api.model
    def _select(self):
        # return super(AccountInvoiceReport, self)._select() + ', line.line_provision_amount, line.line_margin'

        return super(AccountInvoiceReport, self)._select() + """, line.line_provision_amount * 
        (CASE WHEN move.move_type IN ('in_refund','out_refund') THEN -1 ELSE 1 END) AS line_provision_amount, 
        line.line_margin * (CASE WHEN move.move_type IN ('in_refund','out_refund') THEN -1 ELSE 1 END) AS line_margin"""


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    line_margin = fields.Float("Margin", compute='_compute_margin', digits='Product Price', store=True)
    line_provision_amount = fields.Float(string='Provision', store=True)

    @api.depends('price_subtotal', 'quantity')
    def _compute_margin(self):
        for line in self:
            line.line_margin = line.price_subtotal - (line.sale_line_ids.purchase_price * line.quantity)

            if line.price_subtotal and line.move_id.sales_provision_percentage and line.line_margin:
                line.line_provision_amount = (line.line_margin * line.move_id.sales_provision_percentage) / 100
            else:
                line.line_provision_amount = 0.0
