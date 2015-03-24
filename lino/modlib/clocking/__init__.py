# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds functionality for managing worktime clocking.

.. autosummary::
   :toctree:

    models

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."

    verbose_name = _("Clocking")

    def setup_main_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.MySessions')
        m.add_action('clocking.MySessionsByDate')

    def setup_config_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.SessionTypes')

    def setup_explorer_menu(self, site, profile, m):
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('clocking.Sessions')
