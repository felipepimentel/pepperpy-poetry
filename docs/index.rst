Pepperpy Poetry Plugin
====================

.. image:: https://img.shields.io/pypi/v/pepperpy-poetry.svg
   :target: https://pypi.org/project/pepperpy-poetry/
   :alt: PyPI version

.. image:: https://img.shields.io/github/license/felipepimentel/pepperpy-poetry.svg
   :target: https://github.com/felipepimentel/pepperpy-poetry/blob/main/LICENSE
   :alt: License

A Poetry plugin for managing shared configurations and templates across multiple Python projects.

Features
--------

* Shared configuration management with ``pepperpy.toml``
* Template system with inheritance support
* Environment variable management with validation
* Smart configuration caching
* CLI commands for project management

Installation
-----------

You can install the plugin using pip:

.. code-block:: bash

   pip install pepperpy-poetry

Or using Poetry's plugin manager:

.. code-block:: bash

   poetry self add pepperpy-poetry

Usage
-----

List available templates:

.. code-block:: bash

   poetry pepperpy update-deps

Initialize a new project with a template:

.. code-block:: bash

   poetry pepperpy generate-config

Build and serve documentation:

.. code-block:: bash

   poetry pepperpy docs --serve

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started/index
   user-guide/index
   api/index
   contributing/index

API Reference
------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/plugin
   api/config
   api/commands

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 