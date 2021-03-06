# Copyright 2009-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.system`.

"""
from builtins import object

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.modlib.users.mixins import UserAuthored, ByUser
from lino.modlib.office.roles import OfficeUser
from lino.api import dd


class TextFieldTemplate(UserAuthored):

    """A reusable block of text that can be selected from a text editor to
    be inserted into the text being edited.

    """

    class Meta(object):
        verbose_name = _("Text Field Template")
        verbose_name_plural = _("Text Field Templates")

    name = models.CharField(_("Designation"), max_length=200)
    description = dd.RichTextField(_("Description"),
                                   blank=True, null=True, format='plain')
        #~ blank=True,null=True,format='html')
    # team = dd.ForeignKey(
    #     'users.Team', blank=True, null=True,
    #     help_text=_("If not empty, then this template "
    #                 "is reserved to members of this team."))
    text = dd.RichTextField(_("Template Text"),
                            blank=True, null=True, format='html')

    def __unicode__(self):
        return self.name


class TextFieldTemplates(dd.Table):
    model = TextFieldTemplate
    required_roles = dd.required(dd.SiteStaff, OfficeUser)
    insert_layout = dd.FormLayout("""
    name
    user #team
    """, window_size=(60, 'auto'))

    detail_layout = """
    id name user #team
    description
    text
    """


class MyTextFieldTemplates(TextFieldTemplates, ByUser):
    required_roles = dd.required(OfficeUser)
