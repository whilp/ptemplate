from tests import TemplateTest

from ptemplate import CTemplate

class TestCTemplate(TemplateTest):
    cls = CTemplate

    def test_basic(self):
        self.assertProduces("{{foo}}", "bar", {"foo": "bar"})

    # The following are ported from Google's template_unittest.cc,
    # starting around line 400.
    def test_weird_syntax(self):
        # XXX
        #self.assertProduces("hi {{{! VAR {{!VAR} }} lo", "hi { lo")

        self.assertProduces("fn(){{{BI_NEWLINE}} x=4;{{BI_NEWLINE}}}",
            "fn(){\n x=4;\n}")

        # XXX
        #self.assertProduces("{{{{{{VAR}}}}}}}}", "{{{{}}}}}}")

    def test_comment(self):
        self.assertProduces("hi {{!VAR}} lo", "hi  lo")
        self.assertProduces("hi {{!VAR {VAR} }} lo", "hi  lo")
        # XXX
        #self.assertProduces("hi {{! VAR {{!VAR} }} lo", "hi  lo")

    # Skipping TestSetMarkerDelimiters; no plans to support that feature.

    def test_variable(self):
        data = {}
        input = "hi {{VAR}} lo"
        self.assertProduces(input, "hi  lo", data)

        data["VAR"] = "yo"
        self.assertProduces(input, "hi yo lo", data)

        data["VAR"] = "yoyo"
        self.assertProduces(input, "hi yoyo lo", data)

        data["VA"] = "noyo"
        data["VAR "] = "noyo2"
        data["var"] = "noyo3"
        self.assertProduces(input, "hi yoyo lo", data)

    # Skipping TestVariableWithModifiers; modifiers should come eventually.

    def test_section(self):
        data = {}
        # Note: The original test uses whitespace stripping.
        #input = "boo!\nhi {{#SEC}}lo{{#SUBSEC}}jo{{/SUBSEC}}{{/SEC}} bar"
        input = "boo!hi {{#SEC}}lo{{#SUBSEC}}jo{{/SUBSEC}}{{/SEC}} bar\n"
        
        self.assertProduces(input, "boo!hi  bar\n", data)

        data["SEC"]  = [{}]
        self.assertProduces(input, "boo!hi lo bar\n", data)

        data["SUBSEC"] = [{}]
        self.assertProduces(input, "boo!hi lojo bar\n", data)

    # Skipping TestSectionSeparator; separators probably won't be supported in
    # the language itself.

    # Skipping TestInclude; include files probably wont' be supported in the
    # language itself (though it'd be easy).
    # Skipping TestIncludeWithModifiers; see above.
    # Skipping TestRecursiveInclude; see above.

    def test_inheritance(self):
        data = {
            "FOO": "foo",
            "SEC": [{
                "SEC": [{
                    "blah": "blah",
                }]
            }]
        }
        input = "{{FOO}}{{#SEC}}{{FOO}}{{#SEC}}{{FOO}}{{/SEC}}{{/SEC}}"
        self.assertProduces(input, "foofoofoo", data)
