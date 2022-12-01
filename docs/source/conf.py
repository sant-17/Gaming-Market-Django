# Configuration file for the Sphinx documentation builder.
import os
import sys
import django
sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'gaming_market.settings'
django.setup()
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Gaming-market'
copyright = '2022, Santiago_Garcia Orley_Serna Sebastian_Betancur'
author = 'Santiago_Garcia Orley_Serna Sebastian_Betancur'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    
    'sphinx.ext.autodoc', #Genera la documentación a partir de los docstrings del código fuente.
    'sphinx.ext.autosummary', # Genera automáticamente archivos .rst para automatizar todavía más el trabajo que hace autodoc. Usarla o no depende de qué control se quiera tener sobre el resultado final, después explico bien que hace.
    'sphinx.ext.intersphinx', #Permite hacer links entre documentaciones.
    'sphinx.ext.viewcode' #Permite ver el código fuente desde la documentación.
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bizstyle'
html_static_path = ['_static']
