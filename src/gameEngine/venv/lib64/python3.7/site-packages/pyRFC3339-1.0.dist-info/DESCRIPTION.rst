Description
===========

.. image:: https://travis-ci.org/kurtraschke/pyRFC3339.svg?branch=master
    :target: https://travis-ci.org/kurtraschke/pyRFC3339

pyRFC3339 parses and generates :RFC:`3339`-compliant timestamps using `Python <https://www.python.org/>`_ `datetime.datetime <https://docs.python.org/2/library/datetime.html#datetime-objects>`_ objects.

>>> from pyrfc3339 import generate, parse
>>> from datetime import datetime
>>> import pytz
>>> generate(datetime.utcnow().replace(tzinfo=pytz.utc)) #doctest:+ELLIPSIS
'...T...Z'
>>> parse('2009-01-01T10:01:02Z')
datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=<UTC>)
>>> parse('2009-01-01T14:01:02-04:00')
datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=<UTC-04:00>)

Installation
============

To install the latest version from `PyPI <https://pypi.python.org/pypi>`_:

``$ pip install pyRFC3339``

To install the latest development version:

``$ pip install https://github.com/kurtraschke/pyRFC3339/tarball/master#egg=pyRFC3339-dev``

To build the documentation with Sphinx:

#. ``$ pip install Sphinx``
#. ``$ python setup.py build_sphinx``

The documentation is also available online at:

``https://pythonhosted.org/pyRFC3339/``


