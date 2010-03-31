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

    def test_standard_formatter(self):
        data = {"bar": 1}
        input = "foo {bar}"
        pformat = self.formatter.format(input, **data)
        self.assertEqual(pformat, input.format(**data))
