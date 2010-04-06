import string
from collections import namedtuple

__all__ = ["Formatter"]

Section = namedtuple("Section", "name tokens data scopes")
Token = namedtuple("Token", "text field fieldname marker spec conversion")

class Formatter(string.Formatter):
    markers = {
        '#': "startsection",
        '/': "endsection",
        '%': "comment",
    }
    markerlen = 1

    def vformat(self, string, args, kwargs):
        return self._vformat(string, args, kwargs)

    def _vformat(self, string, args, kwargs):
        tokens = self.tokenize(string)
        return self.formatsection(tokens, kwargs)

    def tokenize(self, string):
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
        sections = []
        result = []
        for token in tokens:
            text = token.text
            section = sections and sections[-1] or Section(None, [], {}, [])
            if token.marker == "startsection" and section.name is None:
                # If we're not already tracking a section, track it.
                section = Section(name=token.field, tokens=[], data=data, scopes=scopes)
                sections.append(section)
            elif token.marker == "endsection" and section.name == token.field:
                # If the current section closes, add a text-only token to its
                # list of tokens and format the section.
                if text:
                    section.tokens.append(Token(text, None, None, None, None, None))
                for d in section.data.get(token.field, []):
                    result.append(self.formatsection(section.tokens, d, [data] + scopes))
                sections.pop()
                text = None
            elif section.name is not None:
                # If we're tracking a section, just add the token to its list
                # and move on.
                section.tokens.append(token)
                continue

            if text:
                result.append(text)
            if token.field is None or token.marker in ("startsection", "endsection"):
                continue

            # Perform the usual string formatting on the field.
            obj, _ = self.get_field(token.field, (), [data] + scopes)
            obj = self.convert_field(obj, token.conversion)
            spec = self._vformat(token.spec, (), data)
            result.append(self.format_field(obj, spec))

        return ''.join(result)

    def get_value(self, field, args, scopes):
        _scopes = list(scopes)
        value = ''
        while _scopes and value == '':
            scope = _scopes.pop(0)
            value = scope.get(field, '')

        return value
