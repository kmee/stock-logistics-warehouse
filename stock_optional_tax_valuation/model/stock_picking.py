# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 KMEE (http://www.kmee.com.br)
#    @author Luis Felipe Mileo <mileo@kmee.com.br>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm

class AccountTaxCode(orm.Model):
    _inherit = 'account.tax.code'
    _columns = {
        'tax_valuation': fields.boolean('Valuation this tax',
            help="Mark it for include this tax in stock valuation."),
        }
    _defauls = {
        'tax_valuation': True,
    }

class account_tax(orm.Model):
    _inherit = 'account.tax'
    _columns = {
        'tax_valuation': fields.boolean('Valuation this tax',
            help="Mark it for include this tax in stock valuation."),
        }
    _defauls = {
        'tax_valuation': True,
    }

    def onchange_tax_code_id(self, cr, uid, ids, tax_code_id, context=None):
        result = {'value': {}}
        if not tax_code_id:
            return result
        obj_tax_code = self.pool.get('account.tax.code').browse(cr, uid, tax_code_id)
        if obj_tax_code:
            result['value']['tax_valuation'] = obj_tax_code.tax_valuation
        return result


class stock_partial_picking(orm.TransientModel):
    _inherit = 'stock.partial.picking'

    def _compute_tax(self, cr, uid, line):
        value = 0.0
        tax_obj = self.pool.get('account.tax')
        result = tax_obj.compute_all(
                cr, uid, line.taxes_id, line.price_unit, line.product_qty,
                line.product_id, line.order_id.partner_id)
        for r in result['taxes']:
            tax = self.pool.get('account.tax').browse(cr, uid, r['id'])
            if tax.tax_valuation:
                value += r.get('amount', 0.0)
        return result['total'] + value

    # Overridden to inject the purchase price as true 'cost price' when processing
    # incoming pickings.
    def _product_cost_for_average_update(self, cr, uid, move):
        purchase_line = move.purchase_line_id
        if move.picking_id.purchase_id and purchase_line:
            if any([x.invoice_id.state not in ('draft', 'cancel') for x in purchase_line.invoice_lines]):
                # use price set on validated invoices
                cost = move.price_unit
                for inv_line in purchase_line.invoice_lines:
                    if inv_line.invoice_id.state not in ('draft', 'cancel'):
                        inv_currency = inv_line.invoice_id.currency_id.id
                        company_currency = inv_line.invoice_id.company_id.currency_id.id
                        price = self._compute_tax(cr, uid, inv_line)
                        cost = self.pool.get('res.currency').compute(cr, uid, inv_currency, company_currency, price, round=False, context={'date': inv_line.invoice_id.date_invoice})
                        return {'cost': cost, 'currency': company_currency}
            else:
                # use price set on the purchase order
                pur_currency = purchase_line.order_id.currency_id.id
                company_currency = purchase_line.company_id.currency_id.id
                price = self._compute_tax(cr, uid, purchase_line)
                cost = self.pool.get('res.currency').compute(cr, uid, pur_currency, company_currency, price, round=False, context={'date': purchase_line.date_order})
                return {'cost': cost, 'currency': company_currency}
        return super(stock_partial_picking, self)._product_cost_for_average_update(cr, uid, move)