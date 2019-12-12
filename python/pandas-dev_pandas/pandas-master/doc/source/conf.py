# -*- coding: utf-8 -*-
#
# pandas documentation build configuration file, created by
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import re
import inspect
from pandas.compat import u, PY3

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.append(os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../sphinxext'))

sys.path.extend([

    # numpy standard doc extensions
    os.path.join(os.path.dirname(__file__),
                 '..', '../..',
                 'sphinxext')

])

# -- General configuration -----------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.  sphinxext.

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.doctest',
              'sphinx.ext.extlinks',
              'sphinx.ext.todo',
              'numpydoc', # used to parse numpy-style docstrings for autodoc
              'ipython_sphinxext.ipython_directive',
              'ipython_sphinxext.ipython_console_highlighting',
              'sphinx.ext.intersphinx',
              'sphinx.ext.coverage',
              'sphinx.ext.pngmath',
              'sphinx.ext.ifconfig',
              'sphinx.ext.linkcode',
              ]



with open("index.rst") as f:
    index_rst_lines = f.readlines()

# only include the slow autosummary feature if we're building the API section
# of the docs

# JP: added from sphinxdocs
autosummary_generate = False

if any([re.match("\s*api\s*",l) for l in index_rst_lines]):
    autosummary_generate = True

files_to_delete = []
for f in os.listdir(os.path.dirname(__file__)):
    if not f.endswith('.rst') or f.startswith('.') or os.path.basename(f) == 'index.rst':
        continue

    _file_basename = f.split('.rst')[0]
    _regex_to_match = "\s*{}\s*$".format(_file_basename)
    if not any([re.match(_regex_to_match, line) for line in index_rst_lines]):
        files_to_delete.append(f)

if files_to_delete:
    print("I'm about to DELETE the following:\n%s\n" % list(sorted(files_to_delete)))
    sys.stdout.write("WARNING: I'd like to delete those to speed up processing (yes/no)? ")
    if PY3:
        answer = input()
    else:
        answer = raw_input()

    if answer.lower().strip() in ('y','yes'):
        for f in files_to_delete:
            f = os.path.join(os.path.join(os.path.dirname(__file__),f))
            f= os.path.abspath(f)
            try:
                print("Deleting %s" % f)
                os.unlink(f)
            except:
                print("Error deleting %s" % f)
                pass

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u('pandas')
copyright = u('2008-2014, the pandas development team')

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import pandas

# version = '%s r%s' % (pandas.__version__, svn_version())
version = '%s' % (pandas.__version__)

# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'nature_with_gtoc'

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'statsmodels.css'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['themes']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.

# Add redirect for previously existing API pages (which are now included in
# the API pages as top-level functions) based on a template (GH9911)
moved_api_pages = [
    'pandas.core.common.isnull', 'pandas.core.common.notnull', 'pandas.core.reshape.get_dummies',
    'pandas.tools.merge.concat', 'pandas.tools.merge.merge', 'pandas.tools.pivot.pivot_table',
    'pandas.tseries.tools.to_datetime', 'pandas.io.clipboard.read_clipboard', 'pandas.io.excel.ExcelFile.parse',
    'pandas.io.excel.read_excel', 'pandas.io.html.read_html', 'pandas.io.json.read_json',
    'pandas.io.parsers.read_csv', 'pandas.io.parsers.read_fwf', 'pandas.io.parsers.read_table',
    'pandas.io.pickle.read_pickle', 'pandas.io.pytables.HDFStore.append', 'pandas.io.pytables.HDFStore.get',
    'pandas.io.pytables.HDFStore.put', 'pandas.io.pytables.HDFStore.select', 'pandas.io.pytables.read_hdf',
    'pandas.io.sql.read_sql', 'pandas.io.sql.read_frame', 'pandas.io.sql.write_frame',
    'pandas.io.stata.read_stata']

html_additional_pages = {'generated/' + page: 'api_redirect.html' for page in moved_api_pages}

# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'pandas'


# -- Options for LaTeX output --------------------------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    ('index', 'pandas.tex',
     u('pandas: powerful Python data analysis toolkit'),
     u('Wes McKinney\n\& PyData Development Team'), 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'statsmodels': ('http://www.statsmodels.org/devel/', None),
    'matplotlib': ('http://matplotlib.org/', None),
    'python': ('http://docs.python.org/3', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference', None),
    'py': ('https://pylib.readthedocs.io/en/latest/', None)
}
import glob
autosummary_generate = glob.glob("*.rst")

# extlinks alias
extlinks = {'issue': ('https://github.com/pandas-dev/pandas/issues/%s',
                      'GH'),
            'wiki': ('https://github.com/pandas-dev/pandas/wiki/%s',
                     'wiki ')}

ipython_exec_lines = [
    'import numpy as np',
    'import pandas as pd',
    # This ensures correct rendering on system with console encoding != utf8
    # (windows). It forces pandas to encode its output reprs using utf8
    # whereever the docs are built. The docs' target is the browser, not
    # the console, so this is fine.
    'pd.options.display.encoding="utf8"'
    ]


# Add custom Documenter to handle attributes/methods of an AccessorProperty
# eg pandas.Series.str and pandas.Series.dt (see GH9322)

import sphinx
from sphinx.util import rpartition
from sphinx.ext.autodoc import Documenter, MethodDocumenter, AttributeDocumenter
from sphinx.ext.autosummary import Autosummary


class AccessorDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for accessors.
    """

    objtype = 'accessor'
    directivetype = 'method'

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6

    def format_signature(self):
        # this method gives an error/warning for the accessors, therefore
        # overriding it (accessor has no arguments)
        return ''


class AccessorLevelDocumenter(Documenter):
    """
    Specialized Documenter subclass for objects on accessor level (methods,
    attributes).
    """

    # This is the simple straightforward version
    # modname is None, base the last elements (eg 'hour')
    # and path the part before (eg 'Series.dt')
    # def resolve_name(self, modname, parents, path, base):
    #     modname = 'pandas'
    #     mod_cls = path.rstrip('.')
    #     mod_cls = mod_cls.split('.')
    #
    #     return modname, mod_cls + [base]

    def resolve_name(self, modname, parents, path, base):
        if modname is None:
            if path:
                mod_cls = path.rstrip('.')
            else:
                mod_cls = None
                # if documenting a class-level object without path,
                # there must be a current class, either from a parent
                # auto directive ...
                mod_cls = self.env.temp_data.get('autodoc:class')
                # ... or from a class directive
                if mod_cls is None:
                    mod_cls = self.env.temp_data.get('py:class')
                # ... if still None, there's no way to know
                if mod_cls is None:
                    return None, []
            # HACK: this is added in comparison to ClassLevelDocumenter
            # mod_cls still exists of class.accessor, so an extra
            # rpartition is needed
            modname, accessor = rpartition(mod_cls, '.')
            modname, cls = rpartition(modname, '.')
            parents = [cls, accessor]
            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get('autodoc:module')
            if not modname:
                if sphinx.__version__ > '1.3':
                    modname = self.env.ref_context.get('py:module')
                else:
                    modname = self.env.temp_data.get('py:module')
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):

    objtype = 'accessorattribute'
    directivetype = 'attribute'

    # lower than AttributeDocumenter so this is not chosen for normal attributes
    priority = 0.6

class AccessorMethodDocumenter(AccessorLevelDocumenter, MethodDocumenter):

    objtype = 'accessormethod'
    directivetype = 'method'

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    """
    This documenter lets us removes .__call__ from the method signature for
    callable accessors like Series.plot
    """
    objtype = 'accessorcallable'
    directivetype = 'method'

    # lower than MethodDocumenter; otherwise the doc build prints warnings
    priority = 0.5

    def format_name(self):
        return MethodDocumenter.format_name(self).rstrip('.__call__')


class PandasAutosummary(Autosummary):
    """
    This alternative autosummary class lets us override the table summary for
    Series.plot and DataFrame.plot in the API docs.
    """

    def _replace_pandas_items(self, display_name, sig, summary, real_name):
        # this a hack: ideally we should extract the signature from the
        # .__call__ method instead of hard coding this
        if display_name == 'DataFrame.plot':
            sig = '([x, y, kind, ax, ....])'
            summary = 'DataFrame plotting accessor and method'
        elif display_name == 'Series.plot':
            sig = '([kind, ax, figsize, ....])'
            summary = 'Series plotting accessor and method'
        return (display_name, sig, summary, real_name)

    def get_items(self, names):
        items = Autosummary.get_items(self, names)
        items = [self._replace_pandas_items(*item) for item in items]
        return items


# based on numpy doc/source/conf.py
def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except:
            return None

    try:
        fn = inspect.getsourcefile(obj)
    except:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    fn = os.path.relpath(fn, start=os.path.dirname(pandas.__file__))

    if '+' in pandas.__version__:
        return "http://github.com/pandas-dev/pandas/blob/master/pandas/%s%s" % (
            fn, linespec)
    else:
        return "http://github.com/pandas-dev/pandas/blob/v%s/pandas/%s%s" % (
            pandas.__version__, fn, linespec)


# remove the docstring of the flags attribute (inherited from numpy ndarray)
# because these give doc build errors (see GH issue 5331)
def remove_flags_docstring(app, what, name, obj, options, lines):
    if what == "attribute" and name.endswith(".flags"):
        del lines[:]

def setup(app):
    app.connect("autodoc-process-docstring", remove_flags_docstring)
    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)
    app.add_directive('autosummary', PandasAutosummary)