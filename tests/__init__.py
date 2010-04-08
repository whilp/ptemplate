import unittest
try:
    import unittest2
except ImportError:
    unittest2 = False

import warnings

class BaseTest(unittest.TestCase):

    def skipTest(self, reason):
        pass

if unittest2:
    class BaseTest(unittest2.TestCase):
        
        def __init__(self, methodName="runTest"):
            super(BaseTest, self).__init__(methodName)
            self.addTypeEqualityFunc(str, 'assertMultiLineEqual')

        def skipTest(self, reason):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                super(BaseTest, self).skipTest(reason)

class TemplateTest(BaseTest):
    cls = None

    def assertProduces(self, input, expect, kwargs={}, args=()):
        output = self.cls(template=input).render(kwargs)
        self.assertEqual(expect, output)

class ModifierTest(TemplateTest):
    
    def assertProduces(self, input, expect, kwargs={}, args=(), converters={}):
        templater = self.cls(template=input)
        templater.formatter.converters.update(converters)
        output = templater.render(kwargs)
        self.assertEqual(expect, output)
