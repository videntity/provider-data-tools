import unittest, os, imp




class TestCreateProviderIndexes(unittest.TestCase):

    def test_ensure_provider_indexes(self):

        """Run ensure_provider_indexes should return results """

        indexes = imp.load_source('create_provider_indexes.ensure_provider_indexes', '../pdt/create_provider_indexes')
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")
        output_dir = "test_output"

        result = ensure_provider_indexes(csvfile, output_dir)
        print(response_dict)

if __name__ == '__main__':
    unittest.main()
