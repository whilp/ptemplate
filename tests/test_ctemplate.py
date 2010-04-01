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
