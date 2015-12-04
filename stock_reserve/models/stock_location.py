# -*- coding: utf-8 -*-
# © 2013 Camptocamp, SA - Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockLocation(models.Model):

    _inherit = 'stock.location'

    reserved = fields.Boolean('Reserved',
                              help='This location is to be used for '
                                   'stock that has been reserved.')
