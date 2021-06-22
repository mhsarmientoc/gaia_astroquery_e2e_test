DOC GENERATION

We use Sphinx to generate the python classes documentation

1. Sphinx installation
http://www.sphinx-doc.org/en/master/
http://www.sphinx-doc.org/en/master/usage/installation.html

1.1 Installation with conda
$ conda install sphinx


2. Getting started
http://www.sphinx-doc.org/en/master/usage/quickstart.html

ONLY when starting from scratch. These steps can be skipped now.

2.1 Basic framework 
Create a 'docs' folder and, from this folder, run the following command:
$ sphinx-quickstart

This is an interactive script where soe questions must be answered.

2.2 conf.py 

2.2.1 PYTHONPATH
Uncommment the following lines in order to allow the tool to find the python sources. 
Typically this path is the docs' parent folder:

  import os
  import sys
  sys.path.insert(0, os.path.abspath('..'))

2.2.2 Python autodoc
https://medium.com/@eikonomega/getting-started-with-sphinx-autodoc-part-1-2cebbbca5365

Include the extension 'sphinx.ext.autodoc' in the extensions variable 

We invoke the autodoc plugin from the source/index.rst file. See for example:

  Gaia E2E test for Astroquery
  ============================
  .. automodule:: astroquery_tests.main

2.2.3 Markdown plugin
Install the markdown plugin for sphinx:
$ pip3 install sphinx-markdown-builder

Include the extension 'sphinx_markdown_builder' in th eextension variable

If using recommonmark, make sure you explicitly ignore the build files as they will conflict with the system:

exclude_patterns = [ 'build/*' ]

3. GENERATION
Move into the 'docs' folder and execute the following command: 

$ make markdown or
$ make html

For HTML generation the python path must be explicitly set in the shell:
$ export PYTHONPATH=/home/.../astroquery_tests

Documentation can be found at:
./docs/build/markdown
./docs/build/html


