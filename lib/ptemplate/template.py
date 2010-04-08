from ptemplate.formatter import Formatter

__all__ = ["Template"]

class Template(object):
    options = {}
    preprocessor = None
    converters = {}
    
    def __init__(self, template=''):
        self.template = template
        self.formatter = Formatter()

        for k, v in self.converters.items():
            self.formatter.converters[k] = v

    def render(self, **data):
        template = self.template
        preprocessor = getattr(self, "preprocessor", None)
        if callable(preprocessor):
            template = preprocessor(template)
        return self.formatter.format(template, **data)
