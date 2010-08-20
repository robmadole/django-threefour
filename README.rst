================
django-threefour
================

Purpose
-------

To bring the last mile to BDD testing.  What is that last mile?  The fabled
functional testing in the browser.

My main goal with this project was to bring easy Selenium testing to BDD if:

    * You are using Nose as your test runner
    * You are using Freshen as your BDD test runner
    * You are using Selenium>=2.0a5

Installation
------------

This is a `Nose <http://pypi.python.org/pypi/nose/0.10.4>`_ plugin.  So you need
that to begin with.

The traditional way ::

    easy_install django-threefour

The new way ::

    pip install django-threefour

The bleeding edge

    pip install -e git+http://github.com/robmadole/django-threefour.git#egg=django-threefour

How was this named?
-------------------

Selenium has an atomic number of 34.  So "three" "four".  Yes, I understand this
is reaching a bit but I would rather spend time on the code than naming it.  If
you have a better name send it my way.
