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
{/dne}
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
