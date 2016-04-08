import os, unittest, csv
from pdt.pjson import validate_addresses
from pdt import chop_addresses, flatten_addresses


class TestValidateAdresses(unittest.TestCase):

    def test_run_validate_addresses(self):

        """Run validate_addresses should return errors, if any """
        csv_file = os.path.join( os.path.dirname( __file__),  "first10.csv")
        csvfile_addresses = chop_addresses(csvfile)
        csvfile_addresses_flat = flatten_addresses(csvfile_addresses)


        with open(csvfile_addresses_flat, 'rb') as f:
            reader = csv.reader(f)
            csv_dict = list(reader)



        errors = validate_addresses.validate_address_list(csv_dict, csv)
        self.assertEqual(errors, 0)

if __name__ == '__main__':
    unittest.main()
