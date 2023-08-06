Sphinx Pyppeteer builder
========================

Sphinx Pyppeteer builder is a PDF generator for
`Sphinx <https://www.sphinx-doc.org>`_ without usage
of LaTeX. It uses `Pyppeteer <https://github.com/pyppeteer/pyppeteer>`_,
a wrapper to control a web browser. It supports
Chromium for now.

Install
-------

You can install it with `pip`:

.. code:: bash

   pip install sphinx_pyppeteer_builder

Or with `setup.py`:

.. code:: bash

   python setup.py install
   pyppeteer-install

.. important::

   Do not forget to install chromium-headless via
   pyppeteer with command `pyppeteer-install`.
   Generation will not work without that.

Configuration
-------------

You can configure your output with these options:

- pyppeteer_basename
- pyppeteer_theme
- pyppeteer_theme_options
- pyppeteer_title
- pyppeteer_theme_path
- pyppeteer_short_title
- pyppeteer_style
- pyppeteer_css_files
- pyppeteer_show_copyright
- pyppeteer_show_sphinx

Each one has the same behavior of its equivalent
for `html` builder.

.. warning::

   Some themes need adaptation to work fine with
   this module. Check your CSS.

In addition, you can set `pyppeteer_pdf_options`
var. This dict is passed as is to
`the pdf coroutine <https://pyppeteer.github.io/pyppeteer/reference.html#pyppeteer.page.Page.pdf>`_. Default values are:

.. code:: python

   pyppeeter_pdf_options {
       'printBackground': True,
       'format': 'A4',
       'margin': {
           'top': '20mm',
           'bottom': '20mm',
           'left': '10mm',
           'right': '10mm'
       }
   }


.. warning::

   Path option in `pyppeteer_pdf_options` is ignored.

Use
---

Just launch the following:

.. code:: bash

   make pyppeteer

Why an other PDF builder for Sphinx?
------------------------------------

LaTeX is really hard to use and to personalize.
There's also an other project to make PDF without
LaTeX but it is not based on CSS stylesheets.

Web browser to generate PDF have all new generation
CSS specs implemented. You can use
`sphinx_weasyprint_builder` instead if you
don't want a full browser.

This plugin is just `singlehtml` output with
conversion to PDF.
