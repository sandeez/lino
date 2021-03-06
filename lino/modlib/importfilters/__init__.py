# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Import filters
"""

from lino import ad

from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Import filters")

    def setup_config_menu(config, site, profile, m):
        p = site.plugins.importfilters
        m = m.add_menu('filters', p.verbose_name)
        m.add_action('importfilters.Filters')
        m.add_action('importfilters.Import')

    def setup_explorer_menu(config, site, profile, m):
        p = site.plugins.importfilters
        m = m.add_menu('filters', p.verbose_name)
        m.add_action('importfilters.Filters')
