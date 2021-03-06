# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds functionality for handling plausibility problems.

A plausibility problem is a database integrity problem which is not
visible by the DBMS because detecting it requires higher business
intelligence.  Some plausibility problems can be fixed automatically,
others need human interaction.

The application developer writes **plausibility checkers**,
i.e. pieces of code which contain that business intelligence and which
are attached to a given model.

Examples of plausibility problems are:

- :class:`lino.modlib.countries.models.PlaceChecker`
- :class:`lino_xl.lib.beid.mixins.BeIdCardHolderChecker`
- :class:`lino_xl.lib.addresses.mixins.AddressOwnerChecker`
- :class:`lino.mixins.dupable.DupableChecker`
- :class:`lino_welfare.modlib.pcsw.models.SSINChecker`
- :class:`lino_welfare.modlib.pcsw.models.ClientCoachingsChecker`
- :class:`lino_welfare.modlib.isip.mixins.OverlappingContractsChecker`
- :class:`lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker`



Users automatically get a button "Update plausibility problems" on
objects for which there is at least one checker available.

The application developer can also add a :class:`ProblemsByOwner`
table to the `detail_layout` of any model.


.. autosummary::
   :toctree:

    roles
    choicelists
    models
    fixtures.checkdata
    management.commands.checkdata

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    """See :doc:`/dev/plugins`.

    .. attribute:: responsible_user

        The :attr:`username <lino.modlib.users.models.User.username>`
        of the **main plausibility responsible**, i.e. a designated
        user who will be attributed to plausibility problems for which
        no *specific responible* could be designated (returned by the
        checker's :meth:`get_responsible_user
        <lino.modlib.plausibility.choicelists.Checker.get_responsible_user>`
        method).

        The default value for this is `None`, except on a demo site
        (i.e. which has :attr:`is_demo_site
        <lino.core.site.Site.is_demo_site>` set to `True`) where it is
        ``"'robin'``.

    """
    verbose_name = _("Plausibility")
    needs_plugins = ['lino.modlib.users', 'lino.modlib.gfks']

    # plugin settings
    responsible_user = None  # the username (a string)
    _responsible_user = None  # the cached User object

    def get_responsible_user(self, checker, obj):
        if self.responsible_user is None:
            return None
        if self._responsible_user is None:
            User = self.site.modules.users.User
            try:
                self._responsible_user = User.objects.get(
                    username=self.responsible_user)
            except User.DoesNotExist:
                msg = "Invalid username '{0}' in `responsible_user` "
                msg = msg.format(self.responsible_user)
                raise Exception(msg)
        return self._responsible_user

    def on_site_startup(self, site):
        """Set :attr:`responsible_user` to ``"'robin'`` if this is a demo site
        (:attr:`is_demo_site <lino.core.site.Site.is_demo_site>`).

        """
        super(Plugin, self).on_site_startup(site)
        if site.is_demo_site:
            self.configure(responsible_user='robin')

    def setup_main_menu(self, site, profile, m):
        g = site.plugins.office
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('plausibility.MyProblems')

    def setup_explorer_menu(config, site, profile, m):
        g = site.plugins.system
        m = m.add_menu(g.app_label, g.verbose_name)
        m.add_action('plausibility.Checkers')
        m.add_action('plausibility.AllProblems')
        # m.add_action('plausibility.Severities')
        # m.add_action('plausibility.Feedbacks')

