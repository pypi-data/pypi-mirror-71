=========
Injectify
=========

.. image:: https://img.shields.io/pypi/l/injectify.svg
    :target: https://pypi.org/project/injectify/
.. image:: https://img.shields.io/pypi/v/injectify.svg
    :target: https://pypi.org/project/injectify/
.. image:: https://img.shields.io/pypi/pyversions/cookiecutter.svg
    :target: https://pypi.org/project/injectify/
.. image:: https://api.travis-ci.com/Maltzur/injectify.svg?branch=master
    :target: https://travis-ci.com/Maltzur/injectify
.. image:: https://codecov.io/gh/Maltzur/injectify/branch/master/graphs/badge.svg?branch=master
    :target: https://codecov.io/gh/Maltzur/injectify
.. image:: https://readthedocs.org/projects/injectify/badge/?version=latest
    :target: https://injectify.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/scrutinizer/g/Maltzur/injectify.svg
    :target: https://scrutinizer-ci.com/g/Maltzur/injectify/?branch=master

Injectify is a code injection library that allows you to merge code that you have written into
code from a seprate package.

* Documentation: https://injectify.readthedocs.io
* GitHub: https://github.com/Matlzur/injectify
* PyPi: https://pypi.org/project/injectify

Installing
----------

Install and update using `pipenv`_ (or `pip`_, of course):

.. code-block:: sh

    $ pipenv install injectify

Basic Example
-------------

.. code-block:: python

    from injectify import inject, HeadInjector

    def foo(x):
        return x

    print(foo(10))  # 10

    @inject(target=foo, injector=HeadInjector())
    def handler():
        x = 9000

    print(foo(10))  # 9000

Features
--------

Injectify can inject the following objects:
* classes
* functions
* nested functions
* methods
* modules

.. _pipenv: https://pipenv.kennethreitz.org
.. _pip: https://pip.pypa.io/en/stable/quickstart/
