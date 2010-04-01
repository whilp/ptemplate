from tests import BaseTest

from ptemplate import CTemplate

class TestCTemplate(BaseTest):

    def setUp(self):
        self.template = CTemplate()

    def format(self, string, *args, **kwargs):
        return self.template.format(string, *args, **kwargs)

    def test_basic(self):
        data = {"foo": "bar"}
        input = "{{foo}}"
        self.assertEqual("bar", self.format(input, **data))

    # The following are ported from Google's template_unittest.cc,
    # starting around line 400.
    def test_weird_syntax(self):
        data = {}
        input = "hi {{{! VAR {{!VAR} }} lo"
        # XXX
        #self.assertEqual("hi { lo", self.format(input, **data))

        input = "fn(){{{BI_NEWLINE}} x=4;{{BI_NEWLINE}}}"
        self.assertEqual("fn(){\n x=4;\n}", self.format(input, **data))

        input = "{{{{{{VAR}}}}}}}}"
        # XXX
        #self.assertEqual("{{{{}}}}}}", self.format(input, **data))

    def test_comment(self):
        data = {}
        input = "hi {{!VAR}} lo"
        self.assertEqual("hi  lo", self.format(input, **data))
