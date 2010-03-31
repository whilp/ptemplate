from string import Formatter

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
        section = None
        data = None

        # Define marker here so that it carries over between iterations.
        marker = None
        for text, field, spec, conversion in tokenstream:
            # marker here was defined on the last iteration.
            if marker != "startsection" and not section and text:
                result.append(text)

            if field is None:
                continue

            marker = self.markers.get(field and field[0] or '', None)

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
