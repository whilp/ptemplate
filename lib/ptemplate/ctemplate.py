from ptemplate.template import Template

__all__ = ["CTemplate"]

class CTemplate(Template):

    def preprocessor(self, input):
        input = input.replace("{", "{{")
        input = input.replace("{{{{", "{")
        input = input.replace("}", "}}")
        input = input.replace("}}}}", "}")

        return input
