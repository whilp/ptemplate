import unittest
try:
    import unittest2
except ImportError:
    unittest2 = False

class BaseTest(unittest.TestCase):
    pass

class TemplateTest(BaseTest):
    cls = None

    def setUp(self):
        self.template = self.cls()

    def assertProduces(self, input, expect, kwargs={}, args=()):
        output = self.template.format(input, *args, **kwargs)
        self.assertEqual(expect, output)

if unittest2:
    class BaseTest(unittest2.TestCase):
        
        def __init__(self, methodName="runTest"):
            super(BaseTest, self).__init__(methodName)
            self.addTypeEqualityFunc(str, 'assertMultiLineEqual')
