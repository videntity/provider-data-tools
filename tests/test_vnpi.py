import unittest, os
from pdt.vnpi import verify_npi




class Testvnpi(unittest.TestCase):

    def testRunCSV2PJSON_PUBLIC(self):

        """Run vnpi should return results """

        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        number_processed = 50000

        print(verify_npi(csvfile))

if __name__ == '__main__':
    unittest.main()
