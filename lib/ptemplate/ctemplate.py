"""
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
    options = Template.options.copy()
    options["swallow-return-before-marker"] = False

    def preprocessor(self, input):
        input = input.replace("{", "{{")
        input = input.replace("{{{{", "{")
        input = input.replace("}", "}}")
        input = input.replace("}}}}", "}")

        input = input.replace("{!", "{%")

        return input

    def render(self, **data):
        globals = self.globals.copy()
        globals.update(data)
        return super(CTemplate, self).render(**globals)
