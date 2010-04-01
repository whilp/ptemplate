import unittest
try:
    import unittest2
except ImportError:
    unittest2 = False

class BaseTest(unittest.TestCase):
    pass

if unittest2:
    class BaseTest(unittest2.TestCase):
        
        def __init__(self, methodName="runTest"):
            super(BaseTest, self).__init__(methodName)
            self.addTypeEqualityFunc(str, 'assertMultiLineEqual')
