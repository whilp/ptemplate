from ptemplate.formatter import Formatter

__all__ = ["Template"]

class Template(object):
    options = {}
    preprocessor = None
    converters = {}
    
    def __init__(self, extra_vars_func=None, options=None, template=''):
        self.options = options
        self.template = template
        self.formatter = Formatter()

        for k, v in self.converters.items():
            self.formatter.converters[k] = v

    def render(self, data, format="html", fragment=False, template=None):
        template = self.template
        preprocessor = getattr(self, "preprocessor", None)
        if callable(preprocessor):
            template = preprocessor(template)
        return self.formatter.format(template, **data)

    def transform(self, info, template):
        raise NotImplementedError

    def load_template(self, templatename):
        raise NotImplementedError
