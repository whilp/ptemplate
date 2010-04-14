"""\
:mod:`ptemplate.ctemplate` -- ctemplate-like interface
------------------------------------------------------

This module implements a templating interface similar Google's `ctemplate
<http://google-ctemplate.googlecode.com/>`_ with a few important exceptions:

* templates may not change the field delimiter
* modifiers are marked with '!'
* comments are marked with '%'
* the templater does not strip whitespace (except by modifiers)
* includes are not supported
* pragmas/macros are not supported
* separator sections are not supported

Like ctemplate, :class:`CTemplate` expands a string template to match the
structure of a dictionary (using :class:`ptemplate.template.Template`). Data dictionaries
may contain either lists of other data dictionaries or single values (string,
integer, float, etc). Plain variables are substituted according to the usual
Python string formatting rules (see :pep:`3101`). Sections (fields preceded by
'#') are expanded once for each data dictionary contained in the corresponding
list.
"""

__license__ = """Copyright (c) 2010 Will Maier <will@m.aier.us>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""

from ptemplate.template import Template

__all__ = ["CTemplate"]

class CTemplate(Template):
    """A (somewhat) ctemplate-compatible templater.

    Incompatibilities with Google's ctemplate are documented in
    :mod:`ptemplate.ctemplate`. Construction of a :class:`CTemplate` instance
    is the same as with :class:`ptemplate.template.Template`.
    """
    globals = {
        "BI_NEWLINE": '\n',
        "BI_SPACE": ' ',
    }
    """A global data dictionary.

    Template variables that don't match keys in the main data dictionary may
    match global keys as a last resort. By default, :attr:`globals` contains
    BI_NEWLINE and BI_SPACE, which match the space and newline characters,
    respectively (as in ctemplate).
    """

    def preprocessor(self, input):
        """Convert Google's ctemplate syntax.

        Since ctemplate and :mod:`ptemplate.template` are quite similar
        internally, a simple translation can make a document (mostly) legible.
        At the moment, the preprocessor only converts the marker indicators
        ('{{' and '}}') and comment character ('!').
        """
        input = input.replace("{", "{{")
        input = input.replace("{{{{", "{")
        input = input.replace("}", "}}")
        input = input.replace("}}}}", "}")

        input = input.replace("{!", "{%")

        return input

    def render(self, data, format="html", fragment=False, template=None):
        """Render the template.

        Here, :class:`CTemplate` adds the :attr:`globals` dictionary to the *data*
        dictionary before calling :meth:`ptemplate.template.Template.render`.
        """
        globals = self.globals.copy()
        globals.update(data)
        return super(CTemplate, self).render(globals)
