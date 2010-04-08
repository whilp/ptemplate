"""\
:mod:`ptemplate.ctemplate` -- ctemplate-like interface
------------------------------------------------------

This module implements a templating interface similar Google's _`ctemplate
<http://google-ctemplate.googlecode.com/>` with a few important exceptions:

* templates may not change the field delimiter
* modifiers are marked with '!'
* comments are marked with '%'
* the templater does not strip whitespace (except by modifiers)
* includes are not supported
* pragmas/macros are not supported



Like ctemplate, :class:`CTemplate` expands a string template to match the
structure of a dictionary.k
Data dictionaries may contain either lists of other
data dictionaries or single values (string, integer, float, etc). Plain
variables are substituted according to the usual Python string formatting rules.
Sections (fields preceded by '#') are expanded once for each data dictionary
contained in the corresponding list.

Known differences from Google's ctemplate:
    * no modifiers
    * no whitespace stripping
    * no delimiter setting
"""

from ptemplate.template import Template

__all__ = ["CTemplate"]

class CTemplate(Template):
    globals = {
        "BI_NEWLINE": '\n',
        "BI_SPACE": ' ',
    }

    def preprocessor(self, input):
        input = input.replace("{", "{{")
        input = input.replace("{{{{", "{")
        input = input.replace("}", "}}")
        input = input.replace("}}}}", "}")

        input = input.replace("{!", "{%")

        return input

    def render(self, data, format="html", fragment=False, template=None):
        globals = self.globals.copy()
        globals.update(data)
        return super(CTemplate, self).render(globals)
