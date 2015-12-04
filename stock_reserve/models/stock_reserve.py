# -*- coding: utf-8 -*-
# © 2013 Camptocamp, SA - Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.tools.translate import _


class StockReservation(models.Model):
    """ Allow to reserve products.

    The fields mandatory for the creation of a reservation are:

    * product_id
    * product_uom_qty
    * product_uom
    * name

    The following fields are required but have default values that you may
    want to override:

    * company_id
    * location_id
    * dest_location_id

    Optionally, you may be interested to define:

    * date_validity  (once passed, the reservation will be released)
    * note
    """
    _name = 'stock.reservation'
    _description = 'Stock Reservation'
    _inherits = {'stock.move': 'move_id'}

    move_id = fields.Many2one(
        'stock.move',
        'Reservation Move',
        required=True,
        readonly=True,
        ondelete='cascade',
        select=1)
    date_validity = fields.Date('Validity Date')

    @api.model
    def default_get(self, fields_list):
        """
        Ensure default value of computed field `product_qty` is not set
        as it would raise an error
        """
        res = super(StockReservation, self).default_get(fields_list)
        if 'product_qty' in res:
            del res['product_qty']
        return res

    @api.model
    def _default_picking_type_id(self):
        """ Search for an internal picking type
        """
        type_obj = self.env['stock.picking.type']

        types = type_obj.search([('code', '=', 'internal')], limit=1)
        if types:
            return types[0].id
        return False

    @api.model
    def _default_location_id(self):
        move_obj = self.env['stock.move']
        picking_type_id = self._default_picking_type_id()
        return (move_obj
                .with_context(default_picking_type_id=picking_type_id)
                ._default_location_source())

    @api.model
    def _default_location_dest_id(self):
        location_obj = self.env['stock.location']
        dest_locs = location_obj.search([('reserved', '=', True)], limit=1)
        if dest_locs:
            location_id = dest_locs[0].id
        else:
            location_id = False
        return location_id

    _defaults = {
        'picking_type_id': _default_picking_type_id,
        'location_id': _default_location_id,
        'location_dest_id': _default_location_dest_id,
        'product_uom_qty': 1.0,
    }

    @api.multi
    def reserve(self):
        """ Confirm a reservation

        The reservation is done using the default UOM of the product.
        A date until which the product is reserved can be specified.
        """
        self.date_expected = fields.Datetime.now()
        self.move_id.action_confirm()
        self.move_id.picking_id.action_assign()
        return True

    @api.multi
    def release(self):
        """
        Release moves from reservation
        """
        self.mapped('move_id').action_cancel()
        return True

    @api.model
    def release_validity_exceeded(self, ids=None):
        """ Release all the reservation having an exceeded validity date """
        domain = [('date_validity', '<', fields.date.today()),
                  ('state', '=', 'assigned')]
        if ids:
            domain.append(('id', 'in', ids))
        reserv_ids = self.search(domain)
        reserv_ids.release()
        return True

    @api.multi
    def unlink(self):
        """ Release the reservation before the unlink """
        self.release()
        return super(StockReservation, self).unlink()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ set product_uom and name from product onchange """
        # save value before reading of self.move_id as this last one erase
        # product_id value
        product = self.product_id
        # WARNING this gettattr erase self.product_id
        move = self.move_id
        result = move.onchange_product_id(
            prod_id=product.id, loc_id=False, loc_dest_id=False,
            partner_id=False)
        if result.get('value'):
            vals = result['value']
            # only keep the existing fields on the view
            self.name = vals.get('name')
            self.product_uom = vals.get('product_uom')
            # repeat assignation of product_id so we don't loose it
            self.product_id = product.id

    @api.onchange('product_uom_qty')
    def _onchange_quantity(self):
        """ On change of product quantity avoid negative quantities """
        if not self.product_id or self.product_uom_qty <= 0.0:
            self.product_uom_qty = 0.0

    @api.multi
    def open_move(self):
        assert len(self.ids) == 1, "1 ID expected, got %r" % self.ids
        reserv = self.move_id
        IrModelData = self.env['ir.model.data']
        ref_form2 = 'stock.action_move_form2'
        action = IrModelData.xmlid_to_object(ref_form2)
        action_dict = action.read()[0]
        action_dict['name'] = _('Reservation Move')
        # open directly in the form view
        ref_form = 'stock.view_move_form'
        view_id = IrModelData.xmlid_to_res_id(ref_form)
        action_dict.update(
            views=[(view_id, 'form')],
            res_id=reserv.id,
            )
        return action_dict
