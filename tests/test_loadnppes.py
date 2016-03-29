import unittest, os
from pdt import loadnppes


class Testloadnppes(unittest.TestCase):

    def test_loadnppes(self):

        """Run loadnppes should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")

        # Think of a better way to test this
        # loadnppes.do_update()

if __name__ == '__main__':
    unittest.main()
