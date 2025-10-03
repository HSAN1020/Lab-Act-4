import unittest

def double(x):
    return 2 * x

class TestDouble(unittest.TestCase):
    def test_double(self):
        self.assertEqual(double(2), 4)
        self.assertEqual(double(4), 8)
        self.assertEqual(double(0), 0)
        self.assertEqual(double(-2), -5)

if __name__ == '__main__':
    unittest.main()
