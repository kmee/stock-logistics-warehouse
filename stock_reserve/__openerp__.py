# -*- coding: utf-8 -*-
# © 2013 Camptocamp, SA - Guewen Baconnier
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{'name': 'Stock Reservation',
 'summary': 'Stock reservations on products',
 'version': '8.0.2.0.0',
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'category': 'Warehouse',
 'license': 'AGPL-3',
 'complexity': 'normal',
 'images': [],
 'website': "http://www.camptocamp.com",
 'depends': ['stock',
             ],
 'data': ['views/stock_reserve.xml',
          'views/stock_location.xml',
          'views/product.xml',
          'data/stock_data.xml',
          'security/ir.model.access.csv',
          ],
 'post_init_hook': 'post_init_hook',
 'auto_install': False,
 'tests': ['test/stock_reserve.yml',
          ],
 'installable': True,
 }
