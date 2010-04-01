from collections import namedtuple
from string import Formatter

__all__ = ["Template"]

Section = namedtuple("Section", "name items")

class Field(object):
    markers = {
        '#': "startsection",
        '/': "endsection",
        '%': "comment",
    }
    markerlen = 1
    
    def __init__(self, full):
        self.full = full

    @property
    def name(self):
        if self.marker is None:
            return self.full
        return self.full[self.markerlen:]

    @property
    def marker(self):
        marker = None
        if len(self.full) >= self.markerlen:
            marker = self.full[:self.markerlen]
        return self.markers.get(marker, None)
        
class Template(Formatter):
    options = {
        "swallow-return-before-marker": True,
    }
    preprocessor = None

    def __init__(self, input=''):
        self.input = ''

    def render(self, *args, **data):
        return self.format(self.input, *args, **kwargs)

    def _vformat(self, format_string, args, kwargs, used, depth):
        if depth < 0:
            raise ValueError("Max string recursion exceeded")

        preprocessor = getattr(self, "preprocessor", None)
        if callable(preprocessor):
            format_string = preprocessor(format_string)
        return self.formatsection(self.parse(format_string), kwargs)

    def formatsection(self, tokenstream, *scopes):
        result = []
        sections = []
        data = None
        for text, field, spec, conversion in tokenstream:
            if field is not None:
                field = Field(field)

            if self.options["swallow-return-before-marker"] and \
                field and field.marker and text and text[-1] == '\n':
                text = text[:-1]

            marker = field and field.marker or None
            if marker == "comment":
                field = None
            elif marker == "startsection":
                data = scopes[0].get(field.name, [])
                sections.append(Section(field.name, []))
            elif marker == "endsection":
                if not sections or sections[-1].name != field.name:
                    raise SyntaxError(field.full)
                section = sections[-1]
                section.items.append((text, None, None, None))
                for d in data:
                    result.append(self.formatsection(section.items, d, *scopes))
                del(sections[-1])
                text = ''

            section = sections and sections[-1] or None

            if section is not None and marker != "startsection":
                section.items.append((text, field.name, spec, conversion))
            elif text:
                result.append(text)

            if field is None or field.marker or section is not None:
                continue

            obj, _ = self.get_field(field.name, (), scopes)
            obj = self.convert_field(obj, conversion)
            spec = self._vformat(spec, (), scopes[-1], (), 1)
            result.append(self.format_field(obj, spec))

        return ''.join(result)

    def get_value(self, field, args, scopes):
        for scope in scopes:
            try:
                return super(Template, self).get_value(field, args, scope)
            except KeyError:
                continue
        return ''
