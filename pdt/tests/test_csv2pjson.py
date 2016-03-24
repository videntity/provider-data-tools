import unittest, os
from pdt.csv2pjson_public import publiccsv2pjson



class csv2pjson(unittest.TestCase):
    
    def testRunCSV2PJSONT(self):                          
        
        """Run CSV2pjson should return results """
        
        csvfile = os.path.join( os.path.dirname( __file__),  "fiftythousand.csv")        
        output_dir = "test_output"
        number_processed = 50000
        
        result = publiccsv2pjson(csvfile, output_dir)                 
        self.assertEqual(result['num_files_created'], number_processed)
        
if __name__ == '__main__':
    unittest.main()


