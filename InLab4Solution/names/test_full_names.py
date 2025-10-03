import unittest
from full_names import get_full_name

class NamesTestCase(unittest.TestCase):
    """Tests for full_names.py."""

    def test_first_last(self):
        """Test names like Darth Rowan Samson."""
        full_name = get_full_name('darth rowan', 'samson')
        self.assertEqual(full_name, 'Darth Rowan Samson')

    def test_first_middle_last(self):
        """Test names like Darth Rowan Pongco Samson."""
        full_name = get_full_name('darth rowan', 'samson', 'pongco')
        self.assertEqual(full_name, 'Darth Rowan Pongco Samson')

if __name__ == '__main__':
    unittest.main()
