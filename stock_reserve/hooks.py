# -*- coding: utf-8 -*-
# © 2013 Camptocamp, SA - Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import SUPERUSER_ID


def _default_reservation_location_data(cr, registry, company_id):

    model, record_id = registry['ir.model.data'].get_object_reference(
        cr, SUPERUSER_ID, 'stock', 'stock_location_locations')
    return {
        'name': 'Reservation Stock',
        'reserved': True,
        'location_id': record_id,
        'company_id': company_id,
    }


def post_init_hook(cr, registry):

    # Create one reservation location for each company that does not have one
    location_model = registry['stock.location']
    company_ids = registry['res.company'].search(
        cr, SUPERUSER_ID, [])
    for company_id in company_ids:
        res_loc_id = location_model.search(cr, SUPERUSER_ID,
                                           [('company_id', '=', company_id),
                                            ('reserved', '=', True)])
        if not res_loc_id:
            data = _default_reservation_location_data(cr, registry, company_id)
            registry['stock.location'].create(
                cr, SUPERUSER_ID, data)
