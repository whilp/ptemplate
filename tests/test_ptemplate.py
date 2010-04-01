from tests import BaseTest

from ptemplate import PFormatter

class TestPFormatter(BaseTest):

    def setUp(self):
        self.formatter = PFormatter()
        self.data = {
            "foo": "the foo",
            "results": [
                {"thisis": "letters", "one": "a", "two": "b"},
                {"thisis": "digits", "one": "1", "two": "2"},
            ]
        }
        self.input = """\
{% this is a comment}
la la la
{#results}
this is: {thisis}
this is from a different scope: {foo}

one: {one}
two: {two}
and some more text
{/results}
and something after the section
"""

    def format(self, string, *args, **kwargs):
        return self.formatter.format(string, *args, **kwargs)

    def test_standard_formatter(self):
        data = {"bar": 1}
        input = "foo {bar}"
        self.assertEqual(self.format(input, **data), input.format(**data))

    def test_nonexistent_keys(self):
        self.assertEqual(self.format("{dne}"), "")

    def test_markers_comment(self):
        self.assertEqual(self.format("{% this is a comment}"), "")
        self.assertEqual(self.format("{%this is a comment}"), "")

    def test_markers_section_simple(self):
        data = {
            "section": [
                {"a":"b"}, {}, {},
            ]
        }
        # XXX: need to add section text to results if no vars in section.
        input = '\n'.join([
            "before the section",
            "{#section}",
            "inside the section",
            "some more text",
            "{/section}",
            "and after the section"])
        self.assertEqual(self.format(input, **data), '')


    def test_smorgasbord(self):
        self.assertEqual(self.format(self.input, **self.data), 
            '\n'.join([
            "\nla la la\n",
            "this is: letters",
            "this is from a different scope: the foo\n",
            "one: a",
            "two: b",
            "this is: digits",
            "this is from a different scope: the foo\n",
            "one: 1",
            "two: 2",
            "and something after the section\n"]))
