# -*- coding: utf-8 -*-
# © 2013 Camptocamp, SA - Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reservation_count = fields.Float(
        compute='_reservation_count',
        string='# Sales')

    @api.one
    def _reservation_count(self):
        self.reservation_count = sum(variant.reservation_count
                                     for variant in self.product_variant_ids)

    @api.multi
    def action_view_reservations(self):
        assert len(self._ids) == 1, "Expected 1 ID, got %r" % self._ids
        ref = 'stock_reserve.action_stock_reservation_tree'
        product_ids = self._get_products()
        action_dict = self._get_act_window_dict(ref)
        action_dict['domain'] = [('product_id', 'in', product_ids)]
        action_dict['context'] = {
            'search_default_draft': 1,
            'search_default_reserved': 1
            }
        return action_dict


class ProductProduct(models.Model):
    _inherit = 'product.product'

    reservation_count = fields.Float(
        compute='_reservation_count',
        string='# Sales')

    @api.one
    def _reservation_count(self):
        domain = [('product_id', '=', self.id),
                  ('state', 'in', ['draft', 'assigned'])]
        reservations = self.env['stock.reservation'].search(domain)
        self.reservation_count = sum(reserv.product_qty
                                     for reserv in reservations)

    @api.multi
    def action_view_reservations(self):
        assert len(self._ids) == 1, "Expected 1 ID, got %r" % self._ids
        ref = 'stock_reserve.action_stock_reservation_tree'
        product_id = self._ids[0]
        action_dict = self.product_tmpl_id._get_act_window_dict(ref)
        action_dict['domain'] = [('product_id', '=', product_id)]
        action_dict['context'] = {
            'search_default_draft': 1,
            'search_default_reserved': 1
            }
        return action_dict
