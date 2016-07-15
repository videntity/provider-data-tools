import unittest
import os
from pdt import vnpi


class Testvnpi(unittest.TestCase):

    def test_vnpi(self):
        """Run a real npi and a fake npi to see if True and False """
        self.assertTrue(vnpi.verify_npi(1679576722))
        self.assertFalse(vnpi.verify_npi(1111111111))


if __name__ == '__main__':
    unittest.main()
