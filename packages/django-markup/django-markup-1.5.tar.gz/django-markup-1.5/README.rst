.. image:: https://img.shields.io/pypi/v/django-markup.svg
    :target: https://pypi.org/project/django-markup/

.. image:: https://travis-ci.org/bartTC/django-markup.svg?branch=master
    :target: https://travis-ci.org/bartTC/django-markup

.. image:: https://api.codacy.com/project/badge/Coverage/59e4d38171644acaa13731f08f83ec10
    :target: https://www.codacy.com/app/bartTC/django-markup

.. image:: https://api.codacy.com/project/badge/Grade/59e4d38171644acaa13731f08f83ec10
    :target: https://www.codacy.com/app/bartTC/django-markup

----

📖 Full documentation on https://django-markup.readthedocs.io/en/latest/

=============
django-markup
=============

This app is a generic way to provide filters that convert text into html.

Quickstart
==========

Download and install the package from the python package index (pypi)::

    $ pip install django-markup

Note that `django-markup` ships with some filters ready to use, but the more
complex packages such as Markdown or ReStructuredText are not part of the code.
Please refer the docs which packages are used for the built-in filter.

An alternative is to install django-markup with all filter dependencies
right away. Do so with::

    $ pip install django-markup[all_filter_dependencies]

Then add it to the ``INSTALLED_APPS`` list::

    INSTALLED_APPS = (
        ...
        'django_markup',
    )

Use it in the template::

    {% load markup_tags %}
    {{ the_text|apply_markup:"markdown" }}

Or in Python code::

    from django_markup.markup import formatter
    formatter('Some *Markdown* text.', filter_name='markdown')

Testsuite
=========

To run the testsuite install the project with pipenv and run it::

    % pipenv install --dev
    $ pipenv run test

You can also test against a variation of Django and Python versions
using tox::

    $ tox
