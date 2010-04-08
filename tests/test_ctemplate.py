from tests import TemplateTest

from ptemplate import CTemplate

class TestCTemplate(TemplateTest):
    cls = CTemplate

    def test_basic(self):
        self.assertProduces("{{foo}}", "bar", {"foo": "bar"})

    # The following are ported from Google's template_unittest.cc,
    # starting around line 400.

    def test_weird_syntax_triple_nested(self):
        self.skipTest("needs better-than-naive preprocessor")
        self.assertProduces("hi {{{! VAR {{!VAR} }} lo", "hi { lo")

    def test_weird_syntax_triple(self):
        self.assertProduces("fn(){{{BI_NEWLINE}} x=4;{{BI_NEWLINE}}}",
            "fn(){\n x=4;\n}")

    def test_weird_syntax_tons_of_brackets(self):
        self.skipTest("needs better-than-naive preprocessor")
        self.assertProduces("{{{{{{VAR}}}}}}}}", "{{{{}}}}}}")

    def test_comment(self):
        self.assertProduces("hi {{!VAR}} lo", "hi  lo")

    def test_comment_nested(self):
        self.assertProduces("hi {{!VAR {VAR} }} lo", "hi  lo")

    def test_comment_nested_broken(self):
        self.skipTest("needs better-than-naive preprocessor")
        self.assertProduces("hi {{! VAR {{!VAR} }} lo", "hi  lo")

    # Skipping TestSetMarkerDelimiters; no plans to support that feature.

class TestCTemplateVariables(TemplateTest):
    cls = CTemplate

    def setUp(self):
        self.data = {}
        self.input = "hi {{VAR}} lo"

    def test_variable_nodata(self):
        self.assertProduces(self.input, "hi  lo", self.data)

    def test_variable_simple(self):
        self.data["VAR"] = "yo"
        self.assertProduces(self.input, "hi yo lo", self.data)

    def test_variable_similar(self):
        self.data["VAR"] = "yoyo"
        self.data["VA"] = "noyo"
        self.data["VAR "] = "noyo2"
        self.data["var"] = "noyo3"
        self.assertProduces(self.input, "hi yoyo lo", self.data)

    # Skipping TestVariableWithModifiers; modifiers should come eventually.

class TestCTemplateSection(TemplateTest):
    cls = CTemplate

    def setUp(self):
        self.data = {}
        # Note: The original test uses whitespace stripping.
        #input = "boo!\nhi {{#SEC}}lo{{#SUBSEC}}jo{{/SUBSEC}}{{/SEC}} bar"
        self.input = "boo!hi {{#SEC}}lo{{#SUBSEC}}jo{{/SUBSEC}}{{/SEC}} bar\n"

    def test_section_nodata(self):
        self.assertProduces(self.input, "boo!hi  bar\n", self.data)

    def test_section_outerdata(self):
        self.data["SEC"]  = [{}]
        self.assertProduces(self.input, "boo!hi lo bar\n", self.data)

    def test_section_innerdata(self):
        self.data["SEC"]  = [{}]
        self.data["SUBSEC"] = [{}]
        self.assertProduces(self.input, "boo!hi lojo bar\n", self.data)

    # Skipping TestSectionSeparator; separators probably won't be supported in
    # the language itself.

    # Skipping TestInclude; include files probably wont' be supported in the
    # language itself (though it'd be easy).
    # Skipping TestIncludeWithModifiers; see above.
    # Skipping TestRecursiveInclude; see above.

class TestCTemplateInheritance(TemplateTest):
    cls = CTemplate

    def setUp(self):
        self.data = {
            "FOO": "foo",
            "SEC": [{
                "SEC": [{
                    "blah": "blah",
                }]
            }]
        }
        self.input = "{{FOO}}{{#SEC}}{{FOO}}{{#SEC}}{{FOO}}{{/SEC}}{{/SEC}}\n"

    def test_inheritance(self):
        self.assertProduces(self.input, "foofoofoo\n", self.data)

    def test_inheritance_two_levels(self):
        self.data["SEC"][0]["FOO"] = "bar"
        self.assertProduces(self.input, "foobarbar\n", self.data)

    def test_inheritance_three_levels(self):
        self.data["SEC"][0]["FOO"] = "bar"
        self.data["SEC"][0]["SEC"][0]["FOO"] = "baz"
        self.assertProduces(self.input, "foobarbaz\n", self.data)
