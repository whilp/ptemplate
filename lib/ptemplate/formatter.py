"""\
:mod:`ptemplate.formatter` -- extended string formatter
-------------------------------------------------------

This module extends the advanced string formatter (:pep:`3101`) available in
Python versions greater than 2.5. In addition to regular variable substitution
and formatting, :class:`Formatter` supports sections and in-template comments.
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

import string
from collections import namedtuple

__all__ = ["Formatter", "Section", "Token"]

Section = namedtuple("Section", "name tokens data scopes conversion format")
"""A template section.

Constructor arguments should be passed as keywords and include:

*name* is the name of the section (not including the section marker).

*tokens* is a list of :class:`Token` instances that belong in the section.

*data* is a template data dictionary applicable to the section.

*scopes* is a list of data dictionaries that should be searched successively
when resolving variables in the section.

*conversion* is a conversion string. If not None, it will be passed with the
output of the section to :meth:`Formatter.convert_field`.

*format* is a format string. If not None, it will be passed with the output of
the section to :meth:`Formatter.format_field`.
"""
Token = namedtuple("Token", "text field fieldname marker spec conversion")
"""A template token.

Constructor arguments should be passed as keywords and include:

*text* is the literal text preceding the token.

*field* is the name of the field (or None), not including the marker indicator.

*fieldname* is the full name of the field (or None), including the marker
indicator.

*marker* is a marker type registered in :attr:`Formatter.markers`.

*spec* is a format string passed with the token's contents to
:meth:`Formatter.format_field`.

*conversion* is a conversion string passed with the token's contents to
:meth:`Formatter.convert_field`.
"""

class Formatter(string.Formatter):
    """A string formatter.

    :class:`Formatter` extends the advanced string formatter described in
    :pep:`3101` and implemented in Python versions greater than 2.5. It
    provides hooks that simplify token conversion (:attr:`converters`) and
    recognize special template variables (:attr:`markers`). Since it uses
    :meth:`str._formatter_parser` (implemented in C in the standard interpreter)
    to parse the input string, it should also perform relatively well.
    """
    converters = {}
    """A dictionary of converter functions keyed by conversion strings.

    If a token's conversion string matches a key in this dictionary, :meth:`convert_field`
    will use the converter instead of the usual string conversion.

    .. note::
        
        Keys in this dictionary must be one character in length (to match
        :meth:`str._formatter_parser`'s expectations for format flags).
    """
    markers = {
        '#': "startsection",
        '/': "endsection",
        '%': "comment",
    }
    """A dictionary mapping marker indicators to marker type names.

    The extended syntax supported by :class:`Formatter` is composed of markers
    within normal template variables. Markers registered here can trigger
    extended behavior in :meth:`_vformat`.
    """
    markerlen = 1
    """The length of a marker indicator."""

    def vformat(self, string, args, kwargs):
        """Format *string* according to data in *args* and *kwargs*.

        Unlike :meth:`string.Formatter.vformat`, this method does not track (or
        complain about) unused arguments.
        """
        return self._vformat(string, args, kwargs)

    def _vformat(self, string, args, kwargs):
        """Do the real string formatting.

        This method tokenizes *string* (:meth:`tokenize`) and passes the stream
        of tokens to :meth:`formatsection`, returning the templated string.
        """
        tokens = self.tokenize(string)
        return self.formatsection(tokens, kwargs)

    def tokenize(self, string):
        """Tokenize a template *string*.

        :meth:`tokenize` parses *string* using :meth:`string.Formatter.parse`
        (which in turn relies on :meth:`str._formatter_parser`) and yields
        :class:`Token` instances using the parsed data.
        """
        for text, field, spec, conversion in self.parse(string):
            fieldname = field
            marker = None
            if field and len(field) >= self.markerlen:
                indicator = field[:self.markerlen]
                if indicator in self.markers:
                    marker = self.markers[indicator]
                    field = field[self.markerlen:]
                
            yield Token(text, field, fieldname, marker, spec, conversion)

    def formatsection(self, tokens, data, scopes=[]):
        """Format a section of a token stream according to *data*.

        :meth:`formatsection` builds a formatted string from the iterable *tokens*.
        If it encounters a section in the stream, it creates a new stream and
        passes the section (and everything in it) to another invocation of
        :meth:`formatsection`, adding its output to the formatted string. This
        continues recursively until there are no more sections and the stream of
        tokens is finished. Then, the formatted result is returned.

        When a section is completed, its output will be passed to
        :meth:`convert_field` and :meth:`format_field` if the :attr:`Section.conversion`
        or :attr:`Section.format` attributes were defined, respectively.
        """
        sections = []
        result = []
        depth = 0

        for token in tokens:
            section = sections and sections[-1] or Section(None, [], {}, [], None, None)
            text = token.text

            # Short circuit parsing if...
            if depth == 0 and section.name == token.field and token.marker == "endsection":
                # ...we're closing the topmost section (depth=0); render the
                # subsection and continue.
                section.tokens.append(Token(text, None, None, None, None, None))
                _data, _ = self.get_field(token.field, (), [data] + scopes)
                for d in _data:
                    content = self.formatsection(section.tokens, d, [data] + scopes)
                    if section.conversion:
                        content = self.convert_field(content, section.conversion)
                    if section.format:
                        content = self.format_field(content, section.format)
                    result.append(content)
                sections.pop()
                continue
            elif section.name is not None:
                # ...we're in a section; add our token to the section's list and
                # continue.
                section.tokens.append(token)

                # Track depth (but not the subsections themselves).
                if token.marker == "startsection": depth += 1
                elif token.marker == "endsection": depth -= 1
                continue

            # Always add the token's text to the result. Since the parser produces
            # tokens with preceding text, this has to happen early.
            if text:    
                result.append(text)

            if token.marker == "startsection":
                section = Section(name=token.field, tokens=[], data=data,
                    scopes=scopes, conversion=token.conversion, format=token.spec)
                sections.append(section)
            elif token.marker == "endsection":
                # Already handled.
                pass
            elif token.field is not None:
                # Perform the usual string formatting on the field.
                obj, _ = self.get_field(token.field, (), [data] + scopes)
                obj = self.convert_field(obj, token.conversion)
                spec = super(Formatter, self)._vformat(token.spec, (), data, (), 2)
                result.append(self.format_field(obj, spec))

        return ''.join(result)

    def get_value(self, field, args, scopes):
        """Look up the value of *field* in *scopes*.

        *scopes* is a list of data dictionaries associated with each successive
        parent of the current section. :meth:`get_value` searches for a key
        matching *field* in each of these dictionaries, in order. If no match is
        found, an empty string is returned. Otherwise, the key's value (a list
        of data dictionaries or a string) is returned.
        """
        _scopes = list(scopes)
        value = ''
        while _scopes and value == '':
            scope = _scopes.pop(0)
            value = scope.get(field, '')

        return value

    def convert_field(self, value, conversion):
        """Convert a field *value* according to a *conversion* specification.

        If *conversion* is registered in :attr:`converters`, the *value* is
        passed to the matching converter and the output is returned. Otherwise,
        the *value* and *conversion* specification are passed to
        :meth:`string.Formatter.convert_field`.
        """
        converter = self.converters.get(conversion, None)
        if callable(converter):
            value = converter(value)
        else:
            value = super(Formatter, self).convert_field(value, conversion)
        return value
