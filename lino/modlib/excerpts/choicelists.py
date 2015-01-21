# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This defines the :class:`Shortcuts` choicelist.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _

from lino import dd


class Shortcut(dd.Choice):
    model_spec = None

    def __init__(self, model_spec, name, verbose_name):
        self.model_spec = model_spec
        value = model_spec + "." + name
        super(Shortcut, self).__init__(value, verbose_name, name)


class Shortcuts(dd.ChoiceList):
    verbose_name = _("Excerpt shortcut")
    verbose_name_plural = _("Excerpt shortcuts")
    item_class = Shortcut
    max_length = 50  # fields get created before the values are known
