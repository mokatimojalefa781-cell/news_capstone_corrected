# conf.py for Sphinx documentation

import os
import sys
import django

# 1. Absolute path to your project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

# 2. Set the Django settings module (must match your project folder)
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'

# 3. Initialize Django
django.setup()

# -- Project information -----------------------------------------------------
project = 'News Application'
author = 'Mojalefa Mokati'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',    # Generate documentation from docstrings
    'sphinx.ext.napoleon',   # Support Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
