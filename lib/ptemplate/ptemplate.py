from string import Formatter

__all__ = ["PFormatter"]

class PFormatter(Formatter):
    markers = {
        '#': "startsection",
        '/': "endsection",
        '%': "comment",
    }
    options = {
        "swallow-return-before-marker": True,
    }

    def _vformat(self, format_string, args, kwargs, used, depth):
        if depth < 0:
            raise ValueError("Max string recursion exceeded")

        return self.formatsection(self.parse(format_string), kwargs)

    def formatsection(self, tokenstream, *scopes):
        result = []
        section = data = marker = None
        for text, field, spec, conversion in tokenstream:
            marker = self.markers.get(field and field[0] or '', None)

            if self.options["swallow-return-before-marker"] and \
                marker and text and text[-1] == '\n':
                text = text[:-1]

            if marker == "comment":
                field = None
            elif marker == "startsection":
                data = scopes[0].get(field[1:], [])
                section = []
            elif marker == "endsection":
                if section is None:
                    raise SyntaxError(field)
                section.append((text, None, None, None))
                for d in data:
                    result.append(self.formatsection(section, d, *scopes))
                section = None
                text = ''

            if section is not None and marker != "startsection":
                section.append((text, field, spec, conversion))
            elif text:
                result.append(text)

            if field is None or section is not None:
                continue

            obj, _ = self.get_field(field, (), scopes)
            obj = self.convert_field(obj, conversion)
            spec = self._vformat(spec, (), scopes[-1], (), 1)
            result.append(self.format_field(obj, spec))

        return ''.join(result)

    def get_value(self, field, args, scopes):
        for scope in scopes:
            try:
                return super(PFormatter, self).get_value(field, args, scope)
            except KeyError:
                continue
        return ''
