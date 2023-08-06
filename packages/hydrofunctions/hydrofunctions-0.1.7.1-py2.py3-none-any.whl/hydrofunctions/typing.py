# -*- coding: utf-8 -*-
"""
typing.py

Functions for testing that user input is valid. Why do this instead of standard
python duck typing? These functions are meant to enhance an interactive
session for the user. These functions are meant to check a user's parameters
before requesting data from an onlie resource. Otherwise, the server will
return a 404 code and the user will have no idea why. This tries to raise
an exception (usually a TypeError) before a request is made, so that the user
can fix their request. It also tries to provide a helpful error message to an
interactive session user.

Suggested format for these functions:

* first check that the input is a string,
* then do a regular expression to check that the input is more or less valid.
* raise exceptions when user input breaks format.
"""
from __future__ import absolute_import, print_function
import re


def check_NWIS_bBox(input):
    """Checks that the USGS bBox is valid
    """
    msg = 'NWIS bBox should be a string, list of strings, or tuple ' + \
          'containing the longitude and latitude at the lower left corner ' + \
          'of the bounding box followed by the longitude and latitude ' + \
          'at the upper left corner of the bounding box. Most often in ' + \
          'the form of "ll_long,ll_lat,ur_long,ur_lat" . ' + \
          'Actual value: {}'.format(input)
    if input is None:
        return None
    # assume that if it is a string it will be fine as is.
    # don't accept a series of sites in a single string.
    # Test for and reject empty strings: empty strings are false.
    if isinstance(input, str) and input:
        t = input.split(',')
        if len(t) < 4:
            raise TypeError(msg)
        return input
    # test for input is a list and it is not empty
    elif (isinstance(input, list) or isinstance(input, tuple)) and input:
        if len(input) < 4:
            raise TypeError(msg)
        # format:  [-83.000000, 36.500000, -81.000000, 38.500000] ==> '-83.000000,36.500000,-81.000000,38.500000'
        return ','.join([str(s) for s in input])
    else:
        raise TypeError(msg)


def check_NWIS_site(input):
    """Checks that the USGS station site id is valid.
    """
    msg = "NWIS station id(s) should be a string or list of strings, \
           often in the form of an eight digit number enclosed in quotes. \
           Actual value: {}".format(input)
    output = ""
    if input is None:
        return None
    # assume that if it is a string it will be fine as is.
    # don't accept a series of sites in a single string.
    # Test for and reject empty strings: empty strings are falsy.
    if isinstance(input, str) and input:
        return input
        # input = input.split(',')
    # test for input is a list and it is not empty
    elif isinstance(input, list) and input:
        for s in input:
            if isinstance(s, str) and s:
                output = output + s + ','
            else:
                raise TypeError(msg + "   bad element: {}".format(s))
        # format:  ['0123', '567'] ==> "0123,567"
        # remove the last comma
        return output[:-1]
    else:
        raise TypeError(msg)

    # No longer accept strings with commas.
    # format site(s)
    # sites = '{}'.format(input[0])
    # if len(input) > 1:
    #     for s in input[1:]:
    #         sites += ',{}'.format(s)
    # return sites


def check_NWIS_service(input):
    """Checks that the service is valid: either iv or dv"""
    if input is None:
        return None
    if input == "iv" or input == "dv":
        return input
    else:
        raise TypeError("The NWIS service type accepts 'dv' for daily values, "
                        "or 'iv' for instantaneous values. Actual value: "
                        "{}".format(input))


def check_datestr(input):
    """Checks that the start_date or end_date parameter is in yyyy-mm-dd format.
    """
    # Use a regular expression to ensure in form of yyyy-mm-dd
    if input is None:
        return None
    pattern = r"[1-2]\d\d\d-[0-1]\d-[0-3]\d\Z"
    datestr = re.compile(pattern)
    if isinstance(input, str) and datestr.match(input):
        return input
    else:
        raise TypeError("Dates should be a string in the form of 'YYYY-MM-DD' "
                        "enclosed in quotes. Actual value: {}".format(input))


def check_period(input):
    """Checks that the period parameter in is the P##D format, where ## is
    the number of days before now.
    """
    if input is None:
        return None
    # TODO: check how many days maximum NWIS is willing to respond to.
    # This pattern sets a maximum of 999 days (between 1 and 3 digits).
    pattern = r"^P\d{1,3}D$"
    periodstr = re.compile(pattern)
    if isinstance(input, str) and periodstr.match(input):
        return input
    else:
        raise TypeError("Period should be a string in the form of 'PxD', "
                        "where x represents the number of days before today, "
                        "with a maximum of 999 days. "
                        "Example: to request the previous 10 days, "
                        "enter 'period=P10D'. Actual value entered: {}"
                        .format(input))
