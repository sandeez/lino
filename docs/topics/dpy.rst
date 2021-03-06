.. _dpy:

=====================
The Python serializer
=====================

Lino includes a **Python serializer and deserializer**, one of the
important concepts which Lino adds to a Django project.  It is heavily
used for :doc:`managing and loading demo data </tutorials/dumpy>`, for
:doc:`generating snapshots </dev/dump2py>` and :doc:`migrating
</dev/datamig>` databases.

A **serializer** is run by the `dumpdata
<https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata-appname-appname-appname-model>`__
command and writes data into a file which can be used as a fixture.  A
**deserializer** is run by `loaddata
<https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`__
and loads fixtures into the database.
  
Note also the difference between "intelligent" and "dumped" fixtures:
An **intelligent fixture** is written by a human and used to provide
demo data to a Lino application (see :doc:`/tutorials/dumpy`).  A
**dumped fixture** is generated by the :command:`dumpdata` or
:command:`dump2py` command and looks much less readable because it is
optimized to allow automated database migrations.
  
Concept and implementation of Python fixtures is fully the author's
work, and we didn't yet find a similar approach in any other framework
[#notnew]_. When Luc presented a first draft to the Django developers,
they did not show any interest (ticket `#10664
<http://code.djangoproject.com/ticket/10664>`__). 
But he was convinced enough to continue to use and develop this system.
We still believe that it is genial.



How it works
------------
  
When a Lino application starts up, it sets your `SERIALIZATION_MODULES
<https://docs.djangoproject.com/en/dev/ref/settings/#serialization-modules>`_
setting to `{"py" : "lino.utils.dpy"}`.  This tells Django to
associate the `.py` ending to the :class:`lino.utils.dpy.Deserializer`
class when loading ("deserializing") fixtures.

The :class:`lino.utils.dpy.Deserializer` expects every Python fixture
to define a global function `objects` which it expects to return (or
`yield
<http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained>`_)
the list of model instances to be added to the database.


.. rubric:: Footnotes

.. [#notnew] Though the basic idea of using Python language to
             describe data collections is not new.  For example
             Limodou published a Djangosnippet in 2007 which does
             something similar: `db_dump.py - for dumpping and loading
             data from database
             <http://djangosnippets.org/snippets/14/>`_.
