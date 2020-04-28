#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

if sys.version_info >= (3, 3):
    from unittest.mock import MagicMock
else:
    from mock import MagicMock


class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = [
    'pathlib',
    'sklearn',
    'numpy',
    'scipy',
    'tqdm',
    'tensorflow',
    'toolz',
    'fuzzywuzzy',
    'unidecode',
    'nltk',
    'nltk.tokenize',
    'nltk.util',
    'tensorflow.contrib',
    'tensorflow.contrib.seq2seq',
    'tensorflow.contrib.seq2seq.python',
    'tensorflow.contrib.seq2seq.python.ops',
    'Sastrawi',
    'Sastrawi.Stemmer',
    'Sastrawi.Stemmer.StemmerFactory',
    'xgboost',
    'scipy.sparse',
    'pandas',
    'sklearn.feature_extraction',
    'sklearn.feature_extraction.text',
    'sklearn.metrics',
    'sklearn.metrics.pairwise',
    'sklearn.utils',
    'sklearn.cluster',
    'sklearn.model_selection',
    'sklearn.naive_bayes',
    'sklearn.preprocessing',
    'sklearn.cross_validation',
    'scipy.linalg',
    'sklearn.decomposition',
    'sklearn.pipeline',
    'sklearn.manifold',
    'scipy.cluster',
    'scipy.cluster.hierarchy',
    'scipy.spatial',
    'scipy.spatial.distance',
    'scipy.stats',
    'scipy.stats.mstats',
    'sklearn.neighbors',
    'pulp',
    'ftfy',
    'networkx',
    'bert',
    'dateparser',
    'sentencepiece',
    'tensorflow.keras',
    'tensorflow.keras.preprocessing',
    'tensorflow.keras.preprocessing.sequence',
    'herpetologist',
    'albert',
]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)


# -- Project information -----------------------------------------------------

project = 'malaya'
copyright = '2020, huseinzol05'
author = 'huseinzol05'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
]
numpydoc_show_class_members = False
autodoc_member_order = 'bysource'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    '**.ipynb_checkpoints',
    'Thumbs.db',
    '.DS_Store',
    'load-*.rst',
    '*.ipynb',
    'references.rst',
    'text-clustering-generator.rst',
    'models-accuracy.rst',
    'translator.rst',
    'generate',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

source_suffix = '.rst'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_logo = 'malaya-only.png'


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {'style_nav_header_background': '#fdbe00'}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'malayadoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'malaya.tex', 'malaya Documentation', 'huseinzol05', 'manual')
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, 'malaya', 'malaya Documentation', [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        'malaya',
        'malaya Documentation',
        author,
        'malaya',
        'One line description of project.',
        'Miscellaneous',
    )
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']
