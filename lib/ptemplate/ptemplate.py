from string import Formatter

__all__ = ["PFormatter"]

class PFormatter(Formatter):
    markers = {
        '#': "startsection",
        '/': "endsection",
        '%': "comment",
    }

    def _vformat(self, format_string, args, kwargs, used, depth):
        if depth < 0:
            raise ValueError("Max string recursion exceeded")

        return self.formatsection(self.parse(format_string), kwargs)

    def formatsection(self, tokenstream, *scopes):
        result = []
        section = data = marker = None
        for text, field, spec, conversion in tokenstream:
            oldmarker = marker
            marker = self.markers.get(field and field[0] or '', None)

            if text and not section and not \
                ((section == []) and \
                    (marker is None) and \
                    (oldmarker == "startsection")):
                result.append(text)

            if field is None:
                continue

            # Handle the normal case first.
            if section is None and marker is None:
                obj, _ = self.get_field(field, (), scopes)
                obj = self.convert_field(obj, conversion)
                spec = self._vformat(spec, (), scopes[-1], (), 1)
                result.append(self.format_field(obj, spec))
                continue

            # The field is part of the extended syntax and requires special
            # handling.
            if marker == "comment":
                continue
            elif marker == "startsection":
                data = scopes[0].get(field[1:], [])
                section = []
            elif marker == "endsection":
                if section is None:
                    raise SyntaxError(field)
                for d in data:
                    result.append(self.formatsection(section, d, *scopes))
                section = None

            if section is not None and marker != "startsection":
                section.append((text, field, spec, conversion))

        return ''.join(result)

    def get_value(self, field, args, scopes):
        for scope in scopes:
            try:
                return super(PFormatter, self).get_value(field, args, scope)
            except KeyError:
                continue
        return ''
