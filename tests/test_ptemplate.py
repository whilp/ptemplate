from tests import BaseTest

from ptemplate import PFormatter

class TestPFormatter(BaseTest):

    def setUp(self):
        self.formatter = PFormatter()

    def format(self, string, *args, **kwargs):
        return self.formatter.format(string, *args, **kwargs)

    def test_standard_formatter(self):
        data = {"bar": 1}
        input = "foo {bar}"
        self.assertEqual(input.format(**data), self.format(input, **data))

    def test_nonexistent_keys(self):
        self.assertEqual("", self.format("{dne}"))

    def test_markers_comment(self):
        self.assertEqual("", self.format("{% this is a comment}"))
        self.assertEqual("", self.format("{%this is a comment}"))

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
            "before the section",
            "inside the section",
            "some more text",
            "inside the section",
            "some more text",
            "inside the section",
            "some more text",
            "and after the section"])
        self.assertEqual(output, self.format(input, **data))

    def test_sections_nested(self):
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
        self.assertEqual(output, self.format(input, **data))

    def test_sections_nodata(self):
        data = {}
        input = '\n'.join([
            "beginning",
            "{#section}",
            "middle",
            "{/section}",
            "end"])
        output = '\n'.join([
            "beginning",
            "end"])
        self.assertEqual(output, self.format(input, **data))

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
            "\nla la la",
            "this is: letters",
            "this is from a different scope: the foo",
            "one: a",
            "two: b",
            "and some more text",
            "this is: digits",
            "this is from a different scope: the foo",
            "one: 1",
            "two: 2",
            "and some more text",
            "and something after the section",
        ])
        self.assertEqual(output, self.format(input, **data))
