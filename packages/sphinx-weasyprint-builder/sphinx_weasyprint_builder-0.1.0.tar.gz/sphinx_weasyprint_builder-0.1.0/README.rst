Sphinx WeasyPrint builder
=========================

Sphinx WeasyPrint builder is a PDF generator for
`Sphinx <https://www.sphinx-doc.org>`_ without usage
of LaTeX.

Install
-------

You can install it with `pip`:

.. code:: bash

   pip install sphinx_weasyprint_builder

Or with `setup.py`:

.. code:: bash

   python setup.py install

Configuration
-------------

You can configure your output with these options:

- weasyprint_basename
- weasyprint_theme
- weasyprint_theme_options
- weasyprint_title
- weasyprint_theme_path
- weasyprint_short_title
- weasyprint_style
- weasyprint_css_files
- weasyprint_show_copyright
- weasyprint_show_sphinx

Each one has the same behavior of its equivalent
for `html` builder.

.. warning::

   Your theme must support print media, you can
   have a lot of troubles due to bad CSS. Please
   refer to the WeasyPrint documentation to know
   how to write CSS for printing. For example,
   WeasyPrint can't create scrollbars and some
   text overflows the page.

   You can use the sphinx_weasyprint_theme installed
   with this plugin to start (coming soon!).

In addition, you can set these three variables:

- weasyprint_main_selector
- weasyprint_footer_selector
- weasyprint_header_selector

This builder analyzes generated HTML to extract with
BeautifulSoup a footer and a header. They are removed
from main HTML and reinjected on each page, conforming
to theme's CSS. By default, no header and no footer.

Use compatible selectors for BeautifulSoup.

Use
---

Just launch the following:

.. code:: bash

   make weasyprint

Why an other PDF builder for Sphinx?
------------------------------------

LaTeX is really hard to use and to personalize.
There's also an other project to make PDF without
LaTeX.

WeasyPrint converts HTML to PDF. It's the easiest
way to customize theme and use a constant quality
whatever the media is. If your HTML theme doesn't
have any JavaScript, you can imagine use the same
as HTML and PDF output.

This plugin is just `singlehtml` output with
conversion to PDF.
