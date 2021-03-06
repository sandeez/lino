# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""The :xfile:`models.py` module for the
:mod:`lino.modlib.awesomeuploader` app.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from lino.api import dd, rt


class UploaderAction(dd.Action):

    extjs_main_panel = "Lino.AwesomeUploader()"
    opens_a_window = True
    action_name = 'uploader'
    default_format = 'html'
    # icon_name = 'calendar'


class UploaderPanel(dd.Frame):

    help_text = _("Open an window for multiple file uploads.")
    label = _("Uploader")

    @classmethod
    def get_default_action(self):
        return UploaderAction()


def setup_quicklinks(site, ar, m):
    m.add_action('awesomeuploader.UploaderPanel')


# __all__ = ['UploaderPanel']
