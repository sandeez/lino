# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This initializes the `SITE.jinja_env` object.  Compare with
:mod:`lino.utils.config` which also walks through the `config`
directories. TODO: do only one common loop for both.
"""

from os.path import join, dirname, isdir
import cgi
import jinja2
SUBDIR_NAME = 'config'

from django.conf import settings

from django.utils.translation import ugettext
from django.utils.translation import pgettext
from lino.utils import iif
from lino.utils import format_date
from lino.utils.xmlgen import html as xghtml
from lino.utils.xmlgen.html import E
from lino.utils.jinja import Counter
from lino.core.auth import AnonymousUser

from lino.core.renderer import HtmlRenderer

from lino.api import rt


class JinjaRenderer(HtmlRenderer):
    def __init__(self, *args, **kwargs):
        super(JinjaRenderer, self).__init__(*args, **kwargs)

        loaders = []
        prefix_loaders = {}

        paths = list(settings.SITE.get_settings_subdirs(SUBDIR_NAME))
        if settings.SITE.is_local_project_dir:
            p = join(settings.SITE.project_dir, SUBDIR_NAME)
            if isdir(p):
                paths.append(p)
        #~ logger.info("20130717 web.py paths %s",paths)
        if len(paths) > 0:
            loaders.append(jinja2.FileSystemLoader(paths))

        def func(name, m):
            #~ logger.info("20130717 jinja loader %s %s",name,SUBDIR_NAME)
            if isdir(join(dirname(m.__file__), SUBDIR_NAME)):
                loader = jinja2.PackageLoader(name, SUBDIR_NAME)
                loaders.append(loader)
                prefix_loaders[name] = loader
        settings.SITE.for_each_app(func)

        loaders.insert(0, jinja2.PrefixLoader(prefix_loaders, delimiter=":"))

        #~ loaders = reversed(loaders)
        #~ print 20130109, loaders
        self.jinja_env = jinja2.Environment(
            #~ extensions=['jinja2.ext.i18n'],
            loader=jinja2.ChoiceLoader(loaders))
        #~ jinja_env = jinja2.Environment(trim_blocks=False)

        #~ from django.utils import translation

        #~ jinja_env.install_gettext_translations(translation)

        def as_table(action_spec):
            a = settings.SITE.modules.resolve(action_spec)
            ar = a.request(user=AnonymousUser.instance())
            # 20150810
            # ar.renderer = settings.SITE.plugins.bootstrap3.renderer
            ar.renderer = self

            t = xghtml.Table()
            ar.dump2html(t, ar.sliced_data_iterator)

            #~ print ar.get_total_count()
            return E.tostring(t.as_element())
            #~ return E.tostring(E.ul(*[E.li(ar.summary_row(obj)) for obj in ar]),method="html")

        def as_ul(action_spec):
            a = settings.SITE.modules.resolve(action_spec)
            ar = a.request(user=AnonymousUser.instance())
            # 20150810
            ar.renderer = self
            # ar.renderer = settings.SITE.plugins.bootstrap3.renderer
            return E.tostring(E.ul(*[obj.as_list_item(ar) for obj in ar]))

        self.jinja_env.globals.update(
            settings=settings,
            site=settings.SITE,
            dtos=format_date.fds,  # obsolete
            dtosl=format_date.fdl,  # obsolete
            as_ul=as_ul,
            as_table=as_table,
            iif=iif,
            unicode=unicode,
            len=len,
            E=E,
            # _=_,
            mtos=settings.SITE.decfmt,  # obsolete
            decfmt=settings.SITE.decfmt,
            fds=format_date.fds,
            fdm=format_date.fdm,
            fdl=format_date.fdl,
            fdf=format_date.fdf,
            fdmy=format_date.fdmy,
            babelattr=settings.SITE.babelattr,
            babelitem=settings.SITE.babelitem,  # obsolete
            tr=settings.SITE.babelitem,
            # dd=dd,
            rt=rt,
            escape=cgi.escape,
            Counter=Counter,
            # lino=self.modules,  # experimental
            # site_config=self.site_config,

        )

        def translate(s):
            return ugettext(s.decode('utf8'))
        self.jinja_env.globals.update(_=translate)

        def ptranslate(ctx, s):
            return pgettext(ctx.decode('utf8'), s.decode('utf8'))
        self.jinja_env.globals.update(pgettext=pgettext)

        #~ print __file__, 20121231, self.jinja_env.list_templates('.html')

    def show_table(self, *args, **kwargs):
        e = super(JinjaRenderer, self).show_table(*args, **kwargs)
        return E.tostring(e)
