from tests import TemplateTest

from ptemplate import CTemplate

class TestCTemplate(TemplateTest):
    cls = CTemplate

    def test_basic(self):
        self.produces("{{foo}}", "bar", {"foo": "bar"})

    # The following are ported from Google's template_unittest.cc,
    # starting around line 400.
    def test_weird_syntax(self):
        # XXX
        #self.produces("hi {{{! VAR {{!VAR} }} lo", "hi { lo")

        self.produces("fn(){{{BI_NEWLINE}} x=4;{{BI_NEWLINE}}}",
            "fn(){\n x=4;\n}")

        # XXX
        #self.produces("{{{{{{VAR}}}}}}}}", "{{{{}}}}}}")

    def test_comment(self):
        self.produces("hi {{!VAR}} lo", "hi  lo")
