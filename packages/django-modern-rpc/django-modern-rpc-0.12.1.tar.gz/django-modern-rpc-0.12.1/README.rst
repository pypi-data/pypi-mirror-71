=================
django-modern-rpc
=================

.. image:: https://travis-ci.org/alorence/django-modern-rpc.svg?branch=master
    :alt: Travis-CI (Continuous integration)
    :target: https://travis-ci.org/alorence/django-modern-rpc

.. image:: https://api.codacy.com/project/badge/Grade/3962a60b6911445db8da475614842ea6
    :alt: Codacy (Code quality)
    :target: https://app.codacy.com/app/alorence/django-modern-rpc?utm_source=github.com&utm_medium=referral&utm_content=alorence/django-modern-rpc&utm_campaign=Badge_Grade_Dashboard

.. image:: https://coveralls.io/repos/github/alorence/django-modern-rpc/badge.svg?branch=master
    :alt: Coveralls (coverage report)
    :target: https://coveralls.io/github/alorence/django-modern-rpc?branch=master

.. image:: https://codecov.io/gh/alorence/django-modern-rpc/branch/master/graph/badge.svg
    :alt: Codecov (coverage report)
    :target: https://codecov.io/gh/alorence/django-modern-rpc

.. image:: https://readthedocs.org/projects/django-modern-rpc/badge/?version=latest
    :alt: Read The Doc
    :target: http://django-modern-rpc.readthedocs.io/

.. image:: https://badge.fury.io/py/django-modern-rpc.svg
    :alt: Pypi package info
    :target: https://badge.fury.io/py/django-modern-rpc

.. image:: https://img.shields.io/badge/demo-online-brightgreen.svg
    :alt: Link to online demo
    :target: https://modernrpc.herokuapp.com/

-----------
Description
-----------

Django-modern-rpc provides a simple solution to implement a remote procedure call (RPC) server as part of your Django
project. It supports all major Django and Python versions.

Project's main features are:

- Simple and pythonic API
- Python 2.7 & 3.4+ (Python 2 users must ensure ``six`` package is installed)
- Django 1.8+
- XML-RPC_ and `JSON-RPC 2.0`_ support (JSON-RPC 1.0 not supported)
- HTTP Basic Auth support
- Custom authentication support
- Automatic protocol detection based on request's ``Content-Type`` header
- High-level error management based on exceptions
- Multiple entry points, with specific methods and protocol attached
- RPC Methods documentation generated automatically, based on docstrings
- System introspection methods:

  - system.listMethods()
  - system.methodSignature()
  - system.methodHelp()
  - system.multicall() (XML-RPC only, using specification from https://mirrors.talideon.com/articles/multicall.html)

.. _XML-RPC: http://xmlrpc.scripting.com/
.. _JSON-RPC 2.0: http://www.jsonrpc.org/specification

-----------
Quick start
-----------

#. Use pip to install the package in your environment::

    pip install django-modern-rpc

#. Add it to your Django applications, in ``settings.py``::

    INSTALLED_APPS = [
        ...
        'modernrpc',
    ]

#. Declare an entry point, a view generating correct RPC responses to incoming requests::

    # In myproject/rpc_app/urls.py
    from django.conf.urls import url

    from modernrpc.views import RPCEntryPoint

    urlpatterns = [
        url(r'^rpc/', RPCEntryPoint.as_view()),
    ]

#. Use ``@rpc_method`` to register a global function in django-modern-rpc registry::

    # In myproject/rpc_app/rpc_methods.py
    from modernrpc.core import rpc_method

    @rpc_method
    def add(a, b):
        return a + b

#. Declare the list of python modules containing your RPC methods, in ``settings.py``::

    MODERNRPC_METHODS_MODULES = [
        'rpc_app.rpc_methods'
    ]

Now, you can call the method ``add`` from a client:

.. code:: python

    >>> from xmlrpc.client import ServerProxy
    >>> client = ServerProxy('http://localhost:8000/rpc/')
    >>> print(client.add(2, 3))
    5

For more information, please read `the full documentation`_.

.. _`the full documentation`: http://django-modern-rpc.readthedocs.io
