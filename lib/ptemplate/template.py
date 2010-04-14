"""\
:mod:`ptemplate.template` -- advanced string templating
-------------------------------------------------------

:mod:`ptemplate.template` provides a :class:`Template`, a thin interface on top
:mod:`ptemplate.formatter` that is more useful for typical templating tasks.
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

from ptemplate.formatter import Formatter

__all__ = ["Template"]

class Template(object):
    """A templater.

    :class:`Template` wraps :class:`ptemplate.formatter.Formatter` with a
    _`Buffet`-compatible _`interface`. In addition to the standard Buffet
    arguments (*extra_vars_func*, *options*), the constructor accepts a
    *template* string. This string is the template that will be rendered later
    (by a call to :meth:`render`).

    .. _Buffet:     http://pypi.python.org/pypi/Buffet/
    .. _interface:  http://docs.turbogears.org/1.0/TemplatePlugins
    """
    options = {}
    preprocessor = None
    """Template preprocessor callable.

    This callable should accept the template string as its sole argument. Its
    output should be another template string. Use this facility to translate
    foreign template syntaxes into something
    :class:`ptemplate.formatter.Formatter` can understand.
    """
    converters = {}
    """A dictionary of object converters.

    These converters will be passed to the template's
    :class:`ptemplate.formatter.Formatter` instance.
    """
    
    def __init__(self, extra_vars_func=None, options=None, template=''):
        self.options = options
        self.template = template
        self.formatter = Formatter()
        """The template's formatter.

        The formatter performs the actual templating work and should
        have a :meth:`ptemplate.formatter.Formatter.format` method and a
        :attr:`ptemplate.formatter.Formatter.converters` dictionary. The
        converters dictionary will be updated with any converters specified in
        the Template.
        """

        self.formatter.converters.update(self.converters)

    def render(self, data, format="html", fragment=False, template=None):
        """Render the template using *data*.

        The *format*, *fragment* and *template* arguments are ignored. Instead,
        :class:`Template` uses :attr:`template` as the template, passing it to
        :attr:`preprocessor` if necessary. It then expands the template (using
        :attr:`formatter`) and returns the result as a string.
        """
        template = self.template
        preprocessor = getattr(self, "preprocessor", None)
        if callable(preprocessor):
            template = preprocessor(template)
        return self.formatter.format(template, **data)

    def transform(self, info, template):
        """Render the output to Elements.

        Required by Buffet; not supported.
        """
        raise NotImplementedError

    def load_template(self, templatename):
        """Find a template specified in Python 'dot' notation.

        Required by Buffet; not supported.
        """
        raise NotImplementedError
