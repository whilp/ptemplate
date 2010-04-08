from tests import ModifierTest, TemplateTest

from ptemplate import Template

class TestTemplate(TemplateTest):
    cls = Template

    def test_standard_template(self):
        input = "foo {bar}"
        data = {"bar": 1}
        self.assertProduces(input, input.format(**data), data)

    def test_nonexistent_keys(self):
        self.assertProduces("{dne}", "")

    def test_markers_comment(self):
        self.assertProduces("{%this is a comment}", "")

    def test_markers_comment_space(self):
        self.assertProduces("{% this is a comment}", "")

    def test_sections_simple(self):
        data = {
            "section": [
                {"a":"b"}, {}, {},
            ]
        }
        input = '\n'.join([
            "before the section",
            "{#section}",
            "inside the section",
            "some more text",
            "{/section}",
            "and after the section"])
        output = '\n'.join([
            "before the section\n",
            "inside the section",
            "some more text\n",
            "inside the section",
            "some more text\n",
            "inside the section",
            "some more text\n",
            "and after the section"])
        self.assertProduces(input, output, data)

    def skip_test_sections_nested(self):
        data = {
            "outer": [
                {"inner": [ {} ]},
            ],
        }
        input = '\n'.join([
            "beginning",
            "{#outer}",
            "outer start",
            "{#inner}",
            "inner contents",
            "{/inner}",
            "outer finish",
            "{/outer}"
            "end"])
        output = '\n'.join([
            "beginning",
            "outer start",
            "inner contents",
            "outer finish",
            "end"])
        self.assertProduces(input, output, data)

    def test_sections_nodata(self):
        data = {}
        input = '\n'.join([
            "beginning",
            "{#section}",
            "middle",
            "{/section}",
            "end"])
        output = '\n'.join([
            "beginning\n",
            "end"])
        self.assertProduces(input, output, data)

    def test_smorgasbord(self):
        data = {
            "foo": "the foo",
            "results": [
                {"thisis": "letters", "one": "a", "two": "b"},
                {"thisis": "digits", "one": "1", "two": "2"},
            ]
        }
        input = '\n'.join([
            "{% this is a comment}",
            "la la la",
            "{#results}",
            "this is: {thisis}",
            "this is from a different scope: {foo}",
            "one: {one}",
            "two: {two}",
            "and some more text",
            "{/results}",
            "and something after the section"])
        output = '\n'.join([
            "\nla la la\n",
            "this is: letters",
            "this is from a different scope: the foo",
            "one: a",
            "two: b",
            "and some more text\n",
            "this is: digits",
            "this is from a different scope: the foo",
            "one: 1",
            "two: 2",
            "and some more text\n",
            "and something after the section",
        ])
        self.assertProduces(input, output, data)

class TestModifierHTMLEscape(ModifierTest):
    cls = Template

    def setUp(self):
        import webob
        self.converters = {"h": webob.html_escape}

    def test_modifier_variable_html_escape(self):
        input = """<div class="foo">{foo!h}</div>"""
        data = {"foo": """<a href="http://www.example.com/foo">foo</a>"""}
        output = """<div class="foo">&lt;a href=&quot;http://www.example.com/foo&quot;&gt;foo&lt;/a&gt;</div>"""
        self.assertProduces(input, output, data, converters=self.converters)

    def test_modifier_section_html_escape(self):
        input = """<div class="foo">{#foo!h}inside{bar}{/foo}</div>"""
        data = {"foo": [{"bar": "<p>one!</p>"}, {"bar": "<p>two!</p>"}]}
        output = """<div class="foo">inside&lt;p&gt;one!&lt;/p&gt;inside&lt;p&gt;two!&lt;/p&gt;</div>"""
        self.assertProduces(input, output, data, converters=self.converters)
