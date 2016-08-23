#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Written by Alan Viars

import sys
import json
from luhn import verify

LUHN_PREFIX = "80840"


def verify_npi(number):
    prefixed_number = "%s%s" % (LUHN_PREFIX, number)
    return verify(prefixed_number)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("vnpi.py [NPI]")
        print("Example:")
        print("vnpi.py ")
        sys.exit(1)

    # Get the file from the command line
    result = verify_npi(sys.argv[1])
    jresult = {"number": sys.argv[1], "valid": result}
    print(json.dumps(jresult, indent=4))
