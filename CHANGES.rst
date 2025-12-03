Changelog
=========


Version 0.4.1 (in development)
------------------------------

Fix command-line usage broken in version 0.3, i.e.
``TypeError: calculate() takes 1 positional argument but 5 were given``.


Version 0.4
-----------

Switch to pyproject.toml.

Drop Python 3.7, 3.8, and 3.9 support.

Tag Python 3.11, 3.12, 3.13, and 3.14 support.


Version 0.3.1
-------------

Drop Python 3.6 support.


Version 0.3
-----------

Drop Python 2 support.

Tag Python 3.10 support.


Version 0.2.8
-------------

Fix report LaTeX rendering replacing obsolete ``scrpage2``
with ``scrlayer``-scrpage.

Drop Python 3.5 support.

Tag Python 3.9 support.


Version 0.2.7
-------------

Tag Python 3.8 support.


Version 0.2.6
-------------

Drop Python 3.4 support.


Version 0.2.5
-------------

Raise on non-empty exit code when compiling LaTeX report.

Tag Python 3.7 support.


Version 0.2.4
-------------

Drop Python 3.3 support, add ``python_requires``.


Version 0.2.3
-------------

Tag wheel as universal, include license file.


Version 0.2.2
-------------

Fixed typo in expected spellouts of ``german.yaml`` example.

Ported tests from ``nose``/``unittest`` to ``pytest``.

Use ``os.makedirs(.., exist_ok=True)?? on Python 3.

Update meta data, tag Python 3.6 support.


Version 0.2.1
-------------

Fixed PDF rendering on Linux under Python 3.


Version 0.2
-----------

Added Python 3 support.

More detailed ``--version`` information.


Version 0.1.4
-------------

Fixed PDF-viewer opening functions on Linux and Darwin.


Version 0.1.3
-------------

Fixed broken manual install due to ``setuptools`` automatic
``zip_safe analysis`` not working as expected.


Version 0.1.2
-------------

Added wheel.


Version 0.1.1
-------------

Added support for ``python -m dmengine`` invocation.


Version 0.1
-----------

First public release.
