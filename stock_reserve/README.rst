.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Stock Reservation
=================

Allows to create stock reservations on products.

Each reservation can have a validity date, once passed, the reservation
is automatically lifted.

The reserved products are substracted from the virtual stock. It means
that if you reserved a quantity of products which bring the virtual
stock below the minimum, the orderpoint will be triggered and new
purchase orders will be generated. It also implies that the max may be
exceeded if the reservations are canceled.

If ownership of stock is active in the stock settings, you can specify the
owner on the reservation.

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/153/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/stock-logistics-warehouse/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/stock-logistics-warehouse/issues/new?body=module:%20stock_reserve%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Configuration
=============

A new reserved location is created by default, for the main company. If you
create new companies, you must manually define the corresponding reserved
location and set the flag 'Reserved' in the Location.
=======
Bugs are tracked on `GitHub Issues
<https://github.com/OCA/stock-logistics-warehouse/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
stock-logistics-warehouse/issues/new?body=module:%20
stock_reserve%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Alexandre Fayolle <alexandre.fayolle@camptocamp.com>
* Leonardo Pistone <leonardo.pistone@camptocamp.com>
* Jordi Ballester <jordi.ballester@eficent.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
