import unittest, os, imp
from pdt import chop_nppes_public



class TestChopNppesPublic(unittest.TestCase):

    def test_chop_taxonomy(self):

        """Run ensure_provider_indexes should return results """

        # indexes = imp.load_source('chop_taxonomy', '../pdt/chop_nppes_public')
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        print(chop_nppes_public.chop_taxonomy(csvfile))

if __name__ == '__main__':
    unittest.main()
