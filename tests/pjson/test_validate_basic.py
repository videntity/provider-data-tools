import os, unittest, csv
from pdt.pjson import validate_basic
from pdt import chop_basic


class TestValidateBasic(unittest.TestCase):

    def test_run_validate_basic(self):

        """Run validate_basic should return errors, if any """
        csv_file = os.path.join( os.path.dirname( __file__),  "first10.csv")
        csvfile_basic = chop_basic(csv_file)


        with open(csvfile_basic, 'rb') as f:
            reader = csv.reader(f)
            csv_dict = dict(reader)



        retval = validate_basic.validate_basic_dict(csv_dict, "NP-1", "public")
        print(retval)
if __name__ == '__main__':
    unittest.main()
