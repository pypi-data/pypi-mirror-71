# -*- coding: utf-8 -*-
"""
fixtures_data.py

This file contains sample output from successful requests by hf.NWIS.json()
In otherwords, these are not the raw JSON returned by the NWIS, but rather
the output from calling the .json() method on a Requests object. It actually
isn't json, but rather a Python dict. You can tell because the true and false
in the original json have been coverted to True and False for Python.

The output values included here include:
    - JSON15min2day
    - two_sites_two_params_iv
    - nothing_avail : requested a parameter that doesn't get collected, or filtered sites that collect non-existant param
    - mult_flags : one site, one parameter, three flags: P: provisional, e: estimated, Ice: affected by ice.
    - diff_freq : two sites, several parameters, including pH. The pH are collected every 30 minutes.
"""

JSON15min2day = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://nwis.waterservices.usgs.gov/nwis/iv/format=json%2C1.1&sites=03213700&parameterCd=00060&startDT=2016-09-01&endDT=2016-09-02",
            "criteria": {
                "locationParam": "[ALL:03213700]",
                "variableParam": "[00060]",
                "timeParam": {
                    "beginDateTime": "2016-09-01T00:00:00.000",
                    "endDateTime": "2016-09-02T23:59:59.000",
                },
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:03213700]", "title": "filter:sites"},
                {
                    "value": "[mode=RANGE, modifiedSince=null] interval={INTERVAL[2016-09-01T00:00:00.000-04:00/2016-09-02T23:59:59.000Z]}",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-18T18:40:29.297Z", "title": "requestDT"},
                {"value": "aa1d4ff0-33ac-11e9-a754-3440b59d3362", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "nadww02", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "TUG FORK AT WILLIAMSON, WV",
                    "siteCode": [
                        {"value": "03213700", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 37.67315699,
                            "longitude": -82.2801408,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "05070201", "name": "hucCd"},
                        {"value": "21", "name": "stateCd"},
                        {"value": "21195", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "366",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "363",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T00:15:00.000-04:00",
                            },
                            {
                                "value": "363",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "363",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T00:45:00.000-04:00",
                            },
                            {
                                "value": "363",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "363",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T01:15:00.000-04:00",
                            },
                            {
                                "value": "360",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "357",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T01:45:00.000-04:00",
                            },
                            {
                                "value": "357",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "357",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T02:15:00.000-04:00",
                            },
                            {
                                "value": "357",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "354",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T02:45:00.000-04:00",
                            },
                            {
                                "value": "354",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "354",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T03:15:00.000-04:00",
                            },
                            {
                                "value": "351",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "351",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T03:45:00.000-04:00",
                            },
                            {
                                "value": "351",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "348",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T04:15:00.000-04:00",
                            },
                            {
                                "value": "345",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "345",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T04:45:00.000-04:00",
                            },
                            {
                                "value": "345",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "342",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T05:15:00.000-04:00",
                            },
                            {
                                "value": "339",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "339",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T05:45:00.000-04:00",
                            },
                            {
                                "value": "336",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "336",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T06:15:00.000-04:00",
                            },
                            {
                                "value": "334",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "334",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T06:45:00.000-04:00",
                            },
                            {
                                "value": "334",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "331",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T07:15:00.000-04:00",
                            },
                            {
                                "value": "331",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "331",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T07:45:00.000-04:00",
                            },
                            {
                                "value": "328",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "328",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T08:15:00.000-04:00",
                            },
                            {
                                "value": "325",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "328",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T08:45:00.000-04:00",
                            },
                            {
                                "value": "325",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "325",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T09:15:00.000-04:00",
                            },
                            {
                                "value": "325",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "325",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T09:45:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T10:15:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T10:45:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T11:15:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T11:45:00.000-04:00",
                            },
                            {
                                "value": "322",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T12:15:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T12:45:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T13:15:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T13:45:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T14:15:00.000-04:00",
                            },
                            {
                                "value": "319",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T14:45:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T15:15:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "317",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T15:45:00.000-04:00",
                            },
                            {
                                "value": "314",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "314",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T16:15:00.000-04:00",
                            },
                            {
                                "value": "311",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "311",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T16:45:00.000-04:00",
                            },
                            {
                                "value": "311",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "311",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T17:15:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T17:45:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T18:15:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T18:45:00.000-04:00",
                            },
                            {
                                "value": "308",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T19:15:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T19:45:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T20:15:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T20:45:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "305",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T21:15:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T21:45:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T22:15:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T22:45:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T23:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T23:30:00.000-04:00",
                            },
                            {
                                "value": "303",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-01T23:45:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T00:00:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T00:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T00:30:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T00:45:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T01:00:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T01:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T01:30:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T01:45:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T02:00:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T02:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T02:30:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T02:45:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T03:00:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T03:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T03:30:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T03:45:00.000-04:00",
                            },
                            {
                                "value": "297",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T04:00:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T04:15:00.000-04:00",
                            },
                            {
                                "value": "300",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T04:30:00.000-04:00",
                            },
                            {
                                "value": "297",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T04:45:00.000-04:00",
                            },
                            {
                                "value": "297",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T05:00:00.000-04:00",
                            },
                            {
                                "value": "297",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T05:15:00.000-04:00",
                            },
                            {
                                "value": "297",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T05:30:00.000-04:00",
                            },
                            {
                                "value": "293",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T05:45:00.000-04:00",
                            },
                            {
                                "value": "293",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T06:00:00.000-04:00",
                            },
                            {
                                "value": "293",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T06:15:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T06:30:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T06:45:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T07:00:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T07:15:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T07:30:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T07:45:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T08:00:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T08:15:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T08:30:00.000-04:00",
                            },
                            {
                                "value": "290",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T08:45:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T09:00:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T09:15:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T09:30:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T09:45:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T10:00:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T10:15:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T10:30:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T10:45:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T11:00:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T11:15:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T11:30:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T11:45:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T12:00:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T12:15:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T12:30:00.000-04:00",
                            },
                            {
                                "value": "286",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T12:45:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T13:00:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T13:15:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T13:30:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T13:45:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T14:00:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T14:15:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T14:30:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T14:45:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T15:00:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T15:15:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T15:30:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T15:45:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T16:00:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T16:15:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T16:30:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T16:45:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T17:00:00.000-04:00",
                            },
                            {
                                "value": "283",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T17:15:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T17:30:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T17:45:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T18:00:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T18:15:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T18:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T18:45:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T19:00:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T19:15:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T19:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T19:45:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T20:00:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T20:15:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T20:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T20:45:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T21:00:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T21:15:00.000-04:00",
                            },
                            {
                                "value": "280",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T21:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T21:45:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T22:00:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T22:15:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T22:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T22:45:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T23:00:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T23:15:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T23:30:00.000-04:00",
                            },
                            {
                                "value": "276",
                                "qualifiers": ["A"],
                                "dateTime": "2016-09-02T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 160874}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:03213700:00060:00000",
            }
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}


# XXX: This is just a flag for the start of this data.

two_sites_two_params_iv = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://waterservices.usgs.gov/nwis/iv/format=json&sites=01541000,01541200&period=P1D",
            "criteria": {
                "locationParam": "[ALL:01541000, ALL:01541200]",
                "variableParam": "ALL",
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01541000, ALL:01541200]", "title": "filter:sites"},
                {
                    "value": "[mode=PERIOD, period=P1D, modifiedSince=null]",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-18T18:50:15.142Z", "title": "requestDT"},
                {"value": "074e5150-33ae-11e9-84d1-6cae8b6642ea", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "sdas01", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "974",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:00:00.000-05:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:15:00.000-05:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:30:00.000-05:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:45:00.000-05:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:00:00.000-05:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:15:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:30:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:45:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:00:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:15:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:30:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:45:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:00:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:15:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:30:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:45:00.000-05:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:00:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:15:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:30:00.000-05:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:45:00.000-05:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:00:00.000-05:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:15:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:30:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:45:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:00:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:15:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:30:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:45:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:00:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:15:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:30:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:45:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:00:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:15:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:30:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:45:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:00:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:15:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:30:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:45:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:00:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:15:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:30:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:45:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:00:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:15:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:30:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:45:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:00:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:15:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:30:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:15:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:30:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:15:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:30:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:15:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:30:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:15:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:30:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:45:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:00:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:15:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:30:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:45:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:15:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:30:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:45:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:00:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:15:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:30:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:00:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:15:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:30:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:45:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:00:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:15:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:30:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:45:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:00:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:15:00.000-05:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:30:00.000-05:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:45:00.000-05:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T13:00:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121813}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00060:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00065",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807202,
                            "default": True,
                        }
                    ],
                    "variableName": "Gage height, ft",
                    "variableDescription": "Gage height, feet",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807202",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "6.55",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:00:00.000-05:00",
                            },
                            {
                                "value": "6.54",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:15:00.000-05:00",
                            },
                            {
                                "value": "6.54",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:30:00.000-05:00",
                            },
                            {
                                "value": "6.54",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:45:00.000-05:00",
                            },
                            {
                                "value": "6.54",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:00:00.000-05:00",
                            },
                            {
                                "value": "6.54",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:15:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:30:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:45:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:00:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:15:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:30:00.000-05:00",
                            },
                            {
                                "value": "6.53",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:45:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:00:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:15:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:30:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:45:00.000-05:00",
                            },
                            {
                                "value": "6.51",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:00:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:15:00.000-05:00",
                            },
                            {
                                "value": "6.52",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:30:00.000-05:00",
                            },
                            {
                                "value": "6.51",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:45:00.000-05:00",
                            },
                            {
                                "value": "6.51",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:00:00.000-05:00",
                            },
                            {
                                "value": "6.51",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:15:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:30:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:45:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:00:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:15:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:30:00.000-05:00",
                            },
                            {
                                "value": "6.50",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:45:00.000-05:00",
                            },
                            {
                                "value": "6.49",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:00:00.000-05:00",
                            },
                            {
                                "value": "6.49",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:15:00.000-05:00",
                            },
                            {
                                "value": "6.49",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:30:00.000-05:00",
                            },
                            {
                                "value": "6.49",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:45:00.000-05:00",
                            },
                            {
                                "value": "6.49",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:00:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:15:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:30:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:45:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:00:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:15:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:30:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:45:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:00:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:15:00.000-05:00",
                            },
                            {
                                "value": "6.48",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:30:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:45:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:00:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:15:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:30:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:45:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:00:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:15:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:30:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:45:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:15:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:30:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:45:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:15:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:30:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:45:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:15:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:30:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:45:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:15:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:30:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:45:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:00:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:15:00.000-05:00",
                            },
                            {
                                "value": "6.47",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:30:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:45:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:15:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:30:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:45:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:00:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:15:00.000-05:00",
                            },
                            {
                                "value": "6.46",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:30:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:45:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:00:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:15:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:30:00.000-05:00",
                            },
                            {
                                "value": "6.45",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:45:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:00:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:15:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:30:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:45:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:00:00.000-05:00",
                            },
                            {
                                "value": "6.44",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:15:00.000-05:00",
                            },
                            {
                                "value": "6.43",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:30:00.000-05:00",
                            },
                            {
                                "value": "6.43",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:45:00.000-05:00",
                            },
                            {
                                "value": "6.43",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T13:00:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121814}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00065:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "WB Susquehanna River near Curwensville, PA",
                    "siteCode": [
                        {"value": "01541200", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.9614471,
                            "longitude": -78.5191906,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:45:00.000-05:00",
                            },
                            {
                                "value": "1310",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:45:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:00:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:30:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:15:00.000-05:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:30:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:00:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:15:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:30:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:45:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:00:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:15:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:30:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:45:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:00:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:15:00.000-05:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:30:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:45:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:00:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:15:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:30:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:45:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:00:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:15:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:30:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:45:00.000-05:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T13:00:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121820}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541200:00060:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "WB Susquehanna River near Curwensville, PA",
                    "siteCode": [
                        {"value": "01541200", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.9614471,
                            "longitude": -78.5191906,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00065",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807202,
                            "default": True,
                        }
                    ],
                    "variableName": "Gage height, ft",
                    "variableDescription": "Gage height, feet",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807202",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T14:45:00.000-05:00",
                            },
                            {
                                "value": "4.62",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T15:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T16:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T17:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T18:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T19:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T20:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T21:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T22:45:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:00:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:30:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-17T23:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:15:00.000-05:00",
                            },
                            {
                                "value": "4.61",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T00:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T01:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T02:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T03:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T04:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:30:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T05:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T06:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:00:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T07:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:15:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:30:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T08:45:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:00:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:15:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:30:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T09:45:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:00:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:15:00.000-05:00",
                            },
                            {
                                "value": "4.60",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:30:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T10:45:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:00:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:15:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:30:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T11:45:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:00:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:15:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:30:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T12:45:00.000-05:00",
                            },
                            {
                                "value": "4.59",
                                "qualifiers": ["P"],
                                "dateTime": "2019-02-18T13:00:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121821}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541200:00065:00000",
            },
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}

# XXX: This is just a flag for the start of this data.

nothing_avail = {
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "globalScope": True,
    "name": "ns1:timeSeriesResponseType",
    "nil": False,
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "typeSubstituted": False,
    "value": {
        "queryInfo": {
            "criteria": {
                "locationParam": "[]",
                "parameter": [],
                "variableParam": "[00001]",
            },
            "note": [
                {"title": "filter:stateCd", "value": "[al]"},
                {
                    "title": "filter:timeRange",
                    "value": "[mode=LATEST, modifiedSince=null]",
                },
                {"title": "filter:methodId", "value": "methodIds=[ALL]"},
                {"title": "requestDT", "value": "2019-02-16T03:41:19.226Z"},
                {"title": "requestId", "value": "b8749ca0-319c-11e9-9463-6cae8b6642f6"},
                {
                    "title": "disclaimer",
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                },
                {"title": "server", "value": "caas01"},
            ],
            "queryURL": "http://waterservices.usgs.gov/nwis/iv/format=json&indent=on&stateCd=al&parameterCd=00001&siteStatus=all",
        },
        "timeSeries": [],
    },
}

# XXX: This is just a flag for the start of this data.

mult_flags = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://waterservices.usgs.gov/nwis/iv/format=json&sites=01542500&startDT=2019-01-24&endDT=2019-01-28&parameterCd=00060",
            "criteria": {
                "locationParam": "[ALL:01542500]",
                "variableParam": "[00060]",
                "timeParam": {
                    "beginDateTime": "2019-01-24T00:00:00.000",
                    "endDateTime": "2019-01-28T23:59:59.000",
                },
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01542500]", "title": "filter:sites"},
                {
                    "value": "[mode=RANGE, modifiedSince=null] interval={INTERVAL[2019-01-24T00:00:00.000-05:00/2019-01-28T23:59:59.000Z]}",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-18T17:43:11.924Z", "title": "requestDT"},
                {"value": "a9481f40-33a4-11e9-9bb5-6cae8b663fb6", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "vaas01", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "WB Susquehanna River at Karthaus, PA",
                    "siteCode": [
                        {"value": "01542500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 41.11755906,
                            "longitude": -78.108896,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "2230",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T00:00:00.000-05:00",
                            },
                            {
                                "value": "2210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T00:15:00.000-05:00",
                            },
                            {
                                "value": "2220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T00:30:00.000-05:00",
                            },
                            {
                                "value": "2250",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T00:45:00.000-05:00",
                            },
                            {
                                "value": "2280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T01:00:00.000-05:00",
                            },
                            {
                                "value": "2290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T01:15:00.000-05:00",
                            },
                            {
                                "value": "2300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T01:30:00.000-05:00",
                            },
                            {
                                "value": "2320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T01:45:00.000-05:00",
                            },
                            {
                                "value": "2330",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T02:00:00.000-05:00",
                            },
                            {
                                "value": "2350",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T02:15:00.000-05:00",
                            },
                            {
                                "value": "2380",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T02:30:00.000-05:00",
                            },
                            {
                                "value": "2430",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T02:45:00.000-05:00",
                            },
                            {
                                "value": "2430",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T03:00:00.000-05:00",
                            },
                            {
                                "value": "2500",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T03:15:00.000-05:00",
                            },
                            {
                                "value": "2530",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T03:30:00.000-05:00",
                            },
                            {
                                "value": "2550",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T03:45:00.000-05:00",
                            },
                            {
                                "value": "2570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T04:00:00.000-05:00",
                            },
                            {
                                "value": "2630",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T04:15:00.000-05:00",
                            },
                            {
                                "value": "2640",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T04:30:00.000-05:00",
                            },
                            {
                                "value": "2700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T04:45:00.000-05:00",
                            },
                            {
                                "value": "2730",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T05:00:00.000-05:00",
                            },
                            {
                                "value": "2750",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T05:15:00.000-05:00",
                            },
                            {
                                "value": "2780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T05:30:00.000-05:00",
                            },
                            {
                                "value": "2810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T05:45:00.000-05:00",
                            },
                            {
                                "value": "2850",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T06:00:00.000-05:00",
                            },
                            {
                                "value": "2930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T06:15:00.000-05:00",
                            },
                            {
                                "value": "2990",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T06:30:00.000-05:00",
                            },
                            {
                                "value": "3060",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T06:45:00.000-05:00",
                            },
                            {
                                "value": "3110",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T07:00:00.000-05:00",
                            },
                            {
                                "value": "3150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T07:15:00.000-05:00",
                            },
                            {
                                "value": "3250",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T07:30:00.000-05:00",
                            },
                            {
                                "value": "3310",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T07:45:00.000-05:00",
                            },
                            {
                                "value": "3360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T08:00:00.000-05:00",
                            },
                            {
                                "value": "3440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T08:15:00.000-05:00",
                            },
                            {
                                "value": "3470",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T08:30:00.000-05:00",
                            },
                            {
                                "value": "4040",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T10:30:00.000-05:00",
                            },
                            {
                                "value": "4150",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T12:30:00.000-05:00",
                            },
                            {
                                "value": "4620",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T14:30:00.000-05:00",
                            },
                            {
                                "value": "5270",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T16:30:00.000-05:00",
                            },
                            {
                                "value": "5440",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T18:30:00.000-05:00",
                            },
                            {
                                "value": "5850",
                                "qualifiers": ["P", "e"],
                                "dateTime": "2019-01-24T20:30:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T20:45:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T21:00:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T21:15:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T21:30:00.000-05:00",
                            },
                            {
                                "value": "6070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T21:45:00.000-05:00",
                            },
                            {
                                "value": "6100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T22:00:00.000-05:00",
                            },
                            {
                                "value": "6100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T22:15:00.000-05:00",
                            },
                            {
                                "value": "6100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T22:30:00.000-05:00",
                            },
                            {
                                "value": "6100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T22:45:00.000-05:00",
                            },
                            {
                                "value": "6150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T23:00:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T23:15:00.000-05:00",
                            },
                            {
                                "value": "6120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T23:30:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-24T23:45:00.000-05:00",
                            },
                            {
                                "value": "6070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T00:00:00.000-05:00",
                            },
                            {
                                "value": "6100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T00:15:00.000-05:00",
                            },
                            {
                                "value": "6240",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T00:30:00.000-05:00",
                            },
                            {
                                "value": "6360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T00:45:00.000-05:00",
                            },
                            {
                                "value": "6580",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T01:00:00.000-05:00",
                            },
                            {
                                "value": "6810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T01:15:00.000-05:00",
                            },
                            {
                                "value": "6930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T01:30:00.000-05:00",
                            },
                            {
                                "value": "7180",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T01:45:00.000-05:00",
                            },
                            {
                                "value": "7210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T02:00:00.000-05:00",
                            },
                            {
                                "value": "7360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T02:15:00.000-05:00",
                            },
                            {
                                "value": "7460",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T02:30:00.000-05:00",
                            },
                            {
                                "value": "7510",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T02:45:00.000-05:00",
                            },
                            {
                                "value": "7590",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T03:00:00.000-05:00",
                            },
                            {
                                "value": "7570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T03:15:00.000-05:00",
                            },
                            {
                                "value": "7620",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T03:30:00.000-05:00",
                            },
                            {
                                "value": "7570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T03:45:00.000-05:00",
                            },
                            {
                                "value": "7540",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T04:00:00.000-05:00",
                            },
                            {
                                "value": "7490",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T04:15:00.000-05:00",
                            },
                            {
                                "value": "7380",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T04:30:00.000-05:00",
                            },
                            {
                                "value": "7330",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T04:45:00.000-05:00",
                            },
                            {
                                "value": "7440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T05:00:00.000-05:00",
                            },
                            {
                                "value": "7410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T05:15:00.000-05:00",
                            },
                            {
                                "value": "7490",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T05:30:00.000-05:00",
                            },
                            {
                                "value": "7540",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T05:45:00.000-05:00",
                            },
                            {
                                "value": "7620",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T06:00:00.000-05:00",
                            },
                            {
                                "value": "7670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T06:15:00.000-05:00",
                            },
                            {
                                "value": "7750",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T06:30:00.000-05:00",
                            },
                            {
                                "value": "7780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T06:45:00.000-05:00",
                            },
                            {
                                "value": "7880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T07:00:00.000-05:00",
                            },
                            {
                                "value": "7910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T07:15:00.000-05:00",
                            },
                            {
                                "value": "8070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T07:30:00.000-05:00",
                            },
                            {
                                "value": "8170",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T07:45:00.000-05:00",
                            },
                            {
                                "value": "8150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T08:00:00.000-05:00",
                            },
                            {
                                "value": "8170",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T08:15:00.000-05:00",
                            },
                            {
                                "value": "8230",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T08:30:00.000-05:00",
                            },
                            {
                                "value": "8200",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T08:45:00.000-05:00",
                            },
                            {
                                "value": "8280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T09:00:00.000-05:00",
                            },
                            {
                                "value": "8250",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T09:15:00.000-05:00",
                            },
                            {
                                "value": "8280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T09:30:00.000-05:00",
                            },
                            {
                                "value": "8280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T09:45:00.000-05:00",
                            },
                            {
                                "value": "8230",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T10:00:00.000-05:00",
                            },
                            {
                                "value": "8120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T10:15:00.000-05:00",
                            },
                            {
                                "value": "8280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T10:30:00.000-05:00",
                            },
                            {
                                "value": "8090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T10:45:00.000-05:00",
                            },
                            {
                                "value": "8120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T11:00:00.000-05:00",
                            },
                            {
                                "value": "8200",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T11:15:00.000-05:00",
                            },
                            {
                                "value": "8090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T11:30:00.000-05:00",
                            },
                            {
                                "value": "8070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T11:45:00.000-05:00",
                            },
                            {
                                "value": "8120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T12:00:00.000-05:00",
                            },
                            {
                                "value": "8010",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T12:15:00.000-05:00",
                            },
                            {
                                "value": "8090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T12:30:00.000-05:00",
                            },
                            {
                                "value": "8010",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T12:45:00.000-05:00",
                            },
                            {
                                "value": "8090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T13:00:00.000-05:00",
                            },
                            {
                                "value": "8010",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T13:15:00.000-05:00",
                            },
                            {
                                "value": "8040",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T13:30:00.000-05:00",
                            },
                            {
                                "value": "8070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T13:45:00.000-05:00",
                            },
                            {
                                "value": "8010",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T14:00:00.000-05:00",
                            },
                            {
                                "value": "7930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T14:15:00.000-05:00",
                            },
                            {
                                "value": "7930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T14:30:00.000-05:00",
                            },
                            {
                                "value": "7960",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T14:45:00.000-05:00",
                            },
                            {
                                "value": "7880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T15:00:00.000-05:00",
                            },
                            {
                                "value": "7880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T15:15:00.000-05:00",
                            },
                            {
                                "value": "7800",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T15:30:00.000-05:00",
                            },
                            {
                                "value": "7830",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T15:45:00.000-05:00",
                            },
                            {
                                "value": "7780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T16:00:00.000-05:00",
                            },
                            {
                                "value": "7780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T16:15:00.000-05:00",
                            },
                            {
                                "value": "7830",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T16:30:00.000-05:00",
                            },
                            {
                                "value": "7700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T16:45:00.000-05:00",
                            },
                            {
                                "value": "7780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T17:00:00.000-05:00",
                            },
                            {
                                "value": "7700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T17:15:00.000-05:00",
                            },
                            {
                                "value": "7670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T17:30:00.000-05:00",
                            },
                            {
                                "value": "7640",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T17:45:00.000-05:00",
                            },
                            {
                                "value": "7640",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T18:00:00.000-05:00",
                            },
                            {
                                "value": "7640",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T18:15:00.000-05:00",
                            },
                            {
                                "value": "7590",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T18:30:00.000-05:00",
                            },
                            {
                                "value": "7640",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T18:45:00.000-05:00",
                            },
                            {
                                "value": "7570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T19:00:00.000-05:00",
                            },
                            {
                                "value": "7570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T19:15:00.000-05:00",
                            },
                            {
                                "value": "7540",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T19:30:00.000-05:00",
                            },
                            {
                                "value": "7490",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T19:45:00.000-05:00",
                            },
                            {
                                "value": "7440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T20:00:00.000-05:00",
                            },
                            {
                                "value": "7510",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T20:15:00.000-05:00",
                            },
                            {
                                "value": "7440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T20:30:00.000-05:00",
                            },
                            {
                                "value": "7460",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T20:45:00.000-05:00",
                            },
                            {
                                "value": "7410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T21:00:00.000-05:00",
                            },
                            {
                                "value": "7440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T21:15:00.000-05:00",
                            },
                            {
                                "value": "7360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T21:30:00.000-05:00",
                            },
                            {
                                "value": "7360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T21:45:00.000-05:00",
                            },
                            {
                                "value": "7310",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T22:00:00.000-05:00",
                            },
                            {
                                "value": "7360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T22:15:00.000-05:00",
                            },
                            {
                                "value": "7380",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T22:30:00.000-05:00",
                            },
                            {
                                "value": "7230",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T22:45:00.000-05:00",
                            },
                            {
                                "value": "7280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T23:00:00.000-05:00",
                            },
                            {
                                "value": "7280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T23:15:00.000-05:00",
                            },
                            {
                                "value": "7280",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T23:30:00.000-05:00",
                            },
                            {
                                "value": "7230",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-25T23:45:00.000-05:00",
                            },
                            {
                                "value": "7210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T00:00:00.000-05:00",
                            },
                            {
                                "value": "7210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T00:15:00.000-05:00",
                            },
                            {
                                "value": "7260",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T00:30:00.000-05:00",
                            },
                            {
                                "value": "7180",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T00:45:00.000-05:00",
                            },
                            {
                                "value": "7150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T01:00:00.000-05:00",
                            },
                            {
                                "value": "7180",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T01:15:00.000-05:00",
                            },
                            {
                                "value": "7130",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T01:30:00.000-05:00",
                            },
                            {
                                "value": "7130",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T01:45:00.000-05:00",
                            },
                            {
                                "value": "7100",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T02:00:00.000-05:00",
                            },
                            {
                                "value": "7080",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T02:15:00.000-05:00",
                            },
                            {
                                "value": "7080",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T02:30:00.000-05:00",
                            },
                            {
                                "value": "6980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T02:45:00.000-05:00",
                            },
                            {
                                "value": "6980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T03:00:00.000-05:00",
                            },
                            {
                                "value": "6950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T03:15:00.000-05:00",
                            },
                            {
                                "value": "6930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T03:30:00.000-05:00",
                            },
                            {
                                "value": "6850",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T03:45:00.000-05:00",
                            },
                            {
                                "value": "6880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T04:00:00.000-05:00",
                            },
                            {
                                "value": "6880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T04:15:00.000-05:00",
                            },
                            {
                                "value": "6850",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T04:30:00.000-05:00",
                            },
                            {
                                "value": "6830",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T04:45:00.000-05:00",
                            },
                            {
                                "value": "6780",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T05:00:00.000-05:00",
                            },
                            {
                                "value": "6730",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T05:15:00.000-05:00",
                            },
                            {
                                "value": "6730",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T05:30:00.000-05:00",
                            },
                            {
                                "value": "6710",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T05:45:00.000-05:00",
                            },
                            {
                                "value": "6630",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T06:00:00.000-05:00",
                            },
                            {
                                "value": "6630",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T06:15:00.000-05:00",
                            },
                            {
                                "value": "6630",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T06:30:00.000-05:00",
                            },
                            {
                                "value": "6610",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T06:45:00.000-05:00",
                            },
                            {
                                "value": "6560",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T07:00:00.000-05:00",
                            },
                            {
                                "value": "6560",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T07:15:00.000-05:00",
                            },
                            {
                                "value": "6510",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T07:30:00.000-05:00",
                            },
                            {
                                "value": "6540",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T07:45:00.000-05:00",
                            },
                            {
                                "value": "6510",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T08:00:00.000-05:00",
                            },
                            {
                                "value": "6460",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T08:15:00.000-05:00",
                            },
                            {
                                "value": "6440",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T08:30:00.000-05:00",
                            },
                            {
                                "value": "6490",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T08:45:00.000-05:00",
                            },
                            {
                                "value": "6360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T09:00:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T09:15:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T09:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T09:45:00.000-05:00",
                            },
                            {
                                "value": "6410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T10:00:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T10:15:00.000-05:00",
                            },
                            {
                                "value": "6410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T10:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T10:45:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T11:00:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T11:15:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T11:30:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T11:45:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T12:00:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T12:15:00.000-05:00",
                            },
                            {
                                "value": "6290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T12:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T12:45:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T13:00:00.000-05:00",
                            },
                            {
                                "value": "6290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T13:15:00.000-05:00",
                            },
                            {
                                "value": "6290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T13:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T13:45:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T14:00:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T14:15:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T14:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T14:45:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T15:00:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T15:15:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T15:30:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T15:45:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T16:00:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T16:15:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T16:30:00.000-05:00",
                            },
                            {
                                "value": "6340",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T16:45:00.000-05:00",
                            },
                            {
                                "value": "6290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T17:00:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T17:15:00.000-05:00",
                            },
                            {
                                "value": "6390",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T17:30:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T17:45:00.000-05:00",
                            },
                            {
                                "value": "6360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T18:00:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T18:15:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T18:30:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T18:45:00.000-05:00",
                            },
                            {
                                "value": "6240",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T19:00:00.000-05:00",
                            },
                            {
                                "value": "6320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T19:15:00.000-05:00",
                            },
                            {
                                "value": "6290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T19:30:00.000-05:00",
                            },
                            {
                                "value": "6220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T19:45:00.000-05:00",
                            },
                            {
                                "value": "6220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T20:00:00.000-05:00",
                            },
                            {
                                "value": "6220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T20:15:00.000-05:00",
                            },
                            {
                                "value": "6190",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T20:30:00.000-05:00",
                            },
                            {
                                "value": "6190",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T20:45:00.000-05:00",
                            },
                            {
                                "value": "6150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T21:00:00.000-05:00",
                            },
                            {
                                "value": "6190",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T21:15:00.000-05:00",
                            },
                            {
                                "value": "6150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T21:30:00.000-05:00",
                            },
                            {
                                "value": "6120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T21:45:00.000-05:00",
                            },
                            {
                                "value": "6120",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T22:00:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T22:15:00.000-05:00",
                            },
                            {
                                "value": "6000",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T22:30:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T22:45:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T23:00:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T23:15:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T23:30:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-26T23:45:00.000-05:00",
                            },
                            {
                                "value": "6050",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T00:00:00.000-05:00",
                            },
                            {
                                "value": "6020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T00:15:00.000-05:00",
                            },
                            {
                                "value": "5950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T00:30:00.000-05:00",
                            },
                            {
                                "value": "6000",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T00:45:00.000-05:00",
                            },
                            {
                                "value": "5980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T01:00:00.000-05:00",
                            },
                            {
                                "value": "6000",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T01:15:00.000-05:00",
                            },
                            {
                                "value": "5980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T01:30:00.000-05:00",
                            },
                            {
                                "value": "5950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T01:45:00.000-05:00",
                            },
                            {
                                "value": "5950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T02:00:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T02:15:00.000-05:00",
                            },
                            {
                                "value": "5950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T02:30:00.000-05:00",
                            },
                            {
                                "value": "5980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T02:45:00.000-05:00",
                            },
                            {
                                "value": "5950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T03:00:00.000-05:00",
                            },
                            {
                                "value": "5980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T03:15:00.000-05:00",
                            },
                            {
                                "value": "5980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T03:30:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T03:45:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T04:00:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T04:15:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T04:30:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T04:45:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T05:00:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T05:15:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T05:30:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T05:45:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T06:00:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T06:15:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T06:30:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T06:45:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T07:00:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T07:15:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T07:30:00.000-05:00",
                            },
                            {
                                "value": "5840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T07:45:00.000-05:00",
                            },
                            {
                                "value": "5930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T08:00:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T08:15:00.000-05:00",
                            },
                            {
                                "value": "5880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T08:30:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T08:45:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T09:00:00.000-05:00",
                            },
                            {
                                "value": "5840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T09:15:00.000-05:00",
                            },
                            {
                                "value": "5810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T09:30:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T09:45:00.000-05:00",
                            },
                            {
                                "value": "5910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T10:00:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T10:15:00.000-05:00",
                            },
                            {
                                "value": "5860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T10:30:00.000-05:00",
                            },
                            {
                                "value": "5840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T10:45:00.000-05:00",
                            },
                            {
                                "value": "5810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T11:00:00.000-05:00",
                            },
                            {
                                "value": "5840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T11:15:00.000-05:00",
                            },
                            {
                                "value": "5840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T11:30:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T11:45:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T12:00:00.000-05:00",
                            },
                            {
                                "value": "5810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T12:15:00.000-05:00",
                            },
                            {
                                "value": "5810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T12:30:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T12:45:00.000-05:00",
                            },
                            {
                                "value": "5790",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T13:00:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T13:15:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T13:30:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T13:45:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T14:00:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T14:15:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T14:30:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T14:45:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T15:00:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T15:15:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T15:30:00.000-05:00",
                            },
                            {
                                "value": "5770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T15:45:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T16:00:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T16:15:00.000-05:00",
                            },
                            {
                                "value": "5740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T16:30:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T16:45:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T17:00:00.000-05:00",
                            },
                            {
                                "value": "5700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T17:15:00.000-05:00",
                            },
                            {
                                "value": "5670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T17:30:00.000-05:00",
                            },
                            {
                                "value": "5650",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T17:45:00.000-05:00",
                            },
                            {
                                "value": "5720",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T18:00:00.000-05:00",
                            },
                            {
                                "value": "5670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T18:15:00.000-05:00",
                            },
                            {
                                "value": "5700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T18:30:00.000-05:00",
                            },
                            {
                                "value": "5670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T18:45:00.000-05:00",
                            },
                            {
                                "value": "5700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T19:00:00.000-05:00",
                            },
                            {
                                "value": "5670",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T19:15:00.000-05:00",
                            },
                            {
                                "value": "5650",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T19:30:00.000-05:00",
                            },
                            {
                                "value": "5630",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T19:45:00.000-05:00",
                            },
                            {
                                "value": "5580",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T20:00:00.000-05:00",
                            },
                            {
                                "value": "5580",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T20:15:00.000-05:00",
                            },
                            {
                                "value": "5530",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T20:30:00.000-05:00",
                            },
                            {
                                "value": "5510",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T20:45:00.000-05:00",
                            },
                            {
                                "value": "5470",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T21:00:00.000-05:00",
                            },
                            {
                                "value": "5420",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T21:15:00.000-05:00",
                            },
                            {
                                "value": "5350",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T21:30:00.000-05:00",
                            },
                            {
                                "value": "5290",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T21:45:00.000-05:00",
                            },
                            {
                                "value": "5220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T22:00:00.000-05:00",
                            },
                            {
                                "value": "5220",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T22:15:00.000-05:00",
                            },
                            {
                                "value": "5150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T22:30:00.000-05:00",
                            },
                            {
                                "value": "5060",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T22:45:00.000-05:00",
                            },
                            {
                                "value": "5020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T23:00:00.000-05:00",
                            },
                            {
                                "value": "4950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T23:15:00.000-05:00",
                            },
                            {
                                "value": "4900",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T23:30:00.000-05:00",
                            },
                            {
                                "value": "4860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-27T23:45:00.000-05:00",
                            },
                            {
                                "value": "4770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T00:00:00.000-05:00",
                            },
                            {
                                "value": "4750",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T00:15:00.000-05:00",
                            },
                            {
                                "value": "4700",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T00:30:00.000-05:00",
                            },
                            {
                                "value": "4610",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T00:45:00.000-05:00",
                            },
                            {
                                "value": "4610",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T01:00:00.000-05:00",
                            },
                            {
                                "value": "4570",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T01:15:00.000-05:00",
                            },
                            {
                                "value": "4500",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T01:30:00.000-05:00",
                            },
                            {
                                "value": "4500",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T01:45:00.000-05:00",
                            },
                            {
                                "value": "4480",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T02:00:00.000-05:00",
                            },
                            {
                                "value": "4430",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T02:15:00.000-05:00",
                            },
                            {
                                "value": "4410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T02:30:00.000-05:00",
                            },
                            {
                                "value": "4410",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T02:45:00.000-05:00",
                            },
                            {
                                "value": "4360",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T03:00:00.000-05:00",
                            },
                            {
                                "value": "4320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T03:15:00.000-05:00",
                            },
                            {
                                "value": "4320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T03:30:00.000-05:00",
                            },
                            {
                                "value": "4300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T03:45:00.000-05:00",
                            },
                            {
                                "value": "4270",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T04:00:00.000-05:00",
                            },
                            {
                                "value": "4300",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T04:15:00.000-05:00",
                            },
                            {
                                "value": "4320",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T04:30:00.000-05:00",
                            },
                            {
                                "value": "4250",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T04:45:00.000-05:00",
                            },
                            {
                                "value": "4250",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T05:00:00.000-05:00",
                            },
                            {
                                "value": "4270",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T05:15:00.000-05:00",
                            },
                            {
                                "value": "4210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T05:30:00.000-05:00",
                            },
                            {
                                "value": "4210",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T05:45:00.000-05:00",
                            },
                            {
                                "value": "4170",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T06:00:00.000-05:00",
                            },
                            {
                                "value": "4170",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T06:15:00.000-05:00",
                            },
                            {
                                "value": "4150",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T06:30:00.000-05:00",
                            },
                            {
                                "value": "4170",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T06:45:00.000-05:00",
                            },
                            {
                                "value": "4110",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T07:00:00.000-05:00",
                            },
                            {
                                "value": "4090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T07:15:00.000-05:00",
                            },
                            {
                                "value": "4110",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T07:30:00.000-05:00",
                            },
                            {
                                "value": "4090",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T07:45:00.000-05:00",
                            },
                            {
                                "value": "4110",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T08:00:00.000-05:00",
                            },
                            {
                                "value": "4070",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T08:15:00.000-05:00",
                            },
                            {
                                "value": "4060",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T08:30:00.000-05:00",
                            },
                            {
                                "value": "4020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T08:45:00.000-05:00",
                            },
                            {
                                "value": "4020",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T09:00:00.000-05:00",
                            },
                            {
                                "value": "3980",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T09:15:00.000-05:00",
                            },
                            {
                                "value": "3970",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T09:30:00.000-05:00",
                            },
                            {
                                "value": "3970",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T09:45:00.000-05:00",
                            },
                            {
                                "value": "3970",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T10:00:00.000-05:00",
                            },
                            {
                                "value": "3970",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T10:15:00.000-05:00",
                            },
                            {
                                "value": "3930",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T10:30:00.000-05:00",
                            },
                            {
                                "value": "3950",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T10:45:00.000-05:00",
                            },
                            {
                                "value": "3880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T11:00:00.000-05:00",
                            },
                            {
                                "value": "3910",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T11:15:00.000-05:00",
                            },
                            {
                                "value": "3880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T11:30:00.000-05:00",
                            },
                            {
                                "value": "3860",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T11:45:00.000-05:00",
                            },
                            {
                                "value": "3840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T12:00:00.000-05:00",
                            },
                            {
                                "value": "3880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T12:15:00.000-05:00",
                            },
                            {
                                "value": "3880",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T12:30:00.000-05:00",
                            },
                            {
                                "value": "3840",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T12:45:00.000-05:00",
                            },
                            {
                                "value": "3810",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T13:00:00.000-05:00",
                            },
                            {
                                "value": "3770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T13:15:00.000-05:00",
                            },
                            {
                                "value": "3740",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T13:30:00.000-05:00",
                            },
                            {
                                "value": "3770",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T13:45:00.000-05:00",
                            },
                            {
                                "value": "3760",
                                "qualifiers": ["P"],
                                "dateTime": "2019-01-28T14:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T14:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T14:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T14:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T15:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T15:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T15:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T15:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T16:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T16:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T16:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T16:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T17:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T17:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T17:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T17:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T18:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T18:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T18:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T18:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T19:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T19:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T19:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T19:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T20:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T20:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T20:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T20:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T21:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T21:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T21:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T21:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T22:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T22:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T22:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T22:45:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T23:00:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T23:15:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T23:30:00.000-05:00",
                            },
                            {
                                "value": "-999999",
                                "qualifiers": ["P", "Ice"],
                                "dateTime": "2019-01-28T23:45:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "e",
                                "qualifierDescription": "Value has been estimated.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            },
                            {
                                "qualifierCode": "Ice",
                                "qualifierDescription": "Value is affected by ice at the measurement site.",
                                "qualifierID": 1,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            },
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 2,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            },
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121832}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01542500:00060:00000",
            }
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}

# XXX: flag for start of diff_freq dict.

diff_freq = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://nwis.waterservices.usgs.gov/nwis/iv/format=json&sites=01570500,01541000&startDT=2018-06-01&endDT=2018-06-01",
            "criteria": {
                "locationParam": "[ALL:01570500, ALL:01541000]",
                "variableParam": "ALL",
                "timeParam": {
                    "beginDateTime": "2018-06-01T00:00:00.000",
                    "endDateTime": "2018-06-01T23:59:59.000",
                },
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01570500, ALL:01541000]", "title": "filter:sites"},
                {
                    "value": "[mode=RANGE, modifiedSince=null] interval={INTERVAL[2018-06-01T00:00:00.000-04:00/2018-06-01T23:59:59.000Z]}",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-21T02:51:46.126Z", "title": "requestDT"},
                {"value": "a0801fd0-3583-11e9-a754-3440b59d3362", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "nadww02", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "2540",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "2620",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:15:00.000-04:00",
                            },
                            {
                                "value": "2700",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "2780",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:45:00.000-04:00",
                            },
                            {
                                "value": "2860",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "2920",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:15:00.000-04:00",
                            },
                            {
                                "value": "2960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "2960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:45:00.000-04:00",
                            },
                            {
                                "value": "3020",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "3050",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:15:00.000-04:00",
                            },
                            {
                                "value": "3060",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "3050",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:45:00.000-04:00",
                            },
                            {
                                "value": "3030",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "3010",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:15:00.000-04:00",
                            },
                            {
                                "value": "2990",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "2960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:45:00.000-04:00",
                            },
                            {
                                "value": "2920",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "2860",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:15:00.000-04:00",
                            },
                            {
                                "value": "2860",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "2770",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:45:00.000-04:00",
                            },
                            {
                                "value": "2710",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "2650",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:15:00.000-04:00",
                            },
                            {
                                "value": "2590",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "2530",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:45:00.000-04:00",
                            },
                            {
                                "value": "2470",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "2410",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:15:00.000-04:00",
                            },
                            {
                                "value": "2360",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "2300",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:45:00.000-04:00",
                            },
                            {
                                "value": "2300",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "2200",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:15:00.000-04:00",
                            },
                            {
                                "value": "2150",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "2090",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:45:00.000-04:00",
                            },
                            {
                                "value": "2050",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "2010",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:15:00.000-04:00",
                            },
                            {
                                "value": "1970",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "1930",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:45:00.000-04:00",
                            },
                            {
                                "value": "1890",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "1850",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:15:00.000-04:00",
                            },
                            {
                                "value": "1820",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "1790",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:45:00.000-04:00",
                            },
                            {
                                "value": "1760",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "1730",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:15:00.000-04:00",
                            },
                            {
                                "value": "1710",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "1680",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:45:00.000-04:00",
                            },
                            {
                                "value": "1650",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "1630",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:15:00.000-04:00",
                            },
                            {
                                "value": "1620",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "1590",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:45:00.000-04:00",
                            },
                            {
                                "value": "1580",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "1560",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:15:00.000-04:00",
                            },
                            {
                                "value": "1530",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "1520",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:45:00.000-04:00",
                            },
                            {
                                "value": "1510",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "1490",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:15:00.000-04:00",
                            },
                            {
                                "value": "1480",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "1460",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:45:00.000-04:00",
                            },
                            {
                                "value": "1450",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "1430",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:15:00.000-04:00",
                            },
                            {
                                "value": "1420",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "1410",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:45:00.000-04:00",
                            },
                            {
                                "value": "1390",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "1380",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:15:00.000-04:00",
                            },
                            {
                                "value": "1360",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "1360",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:45:00.000-04:00",
                            },
                            {
                                "value": "1340",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "1330",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:15:00.000-04:00",
                            },
                            {
                                "value": "1320",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "1310",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:45:00.000-04:00",
                            },
                            {
                                "value": "1300",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "1290",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:15:00.000-04:00",
                            },
                            {
                                "value": "1280",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "1270",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:45:00.000-04:00",
                            },
                            {
                                "value": "1260",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "1250",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:15:00.000-04:00",
                            },
                            {
                                "value": "1250",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "1230",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:45:00.000-04:00",
                            },
                            {
                                "value": "1220",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "1220",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:15:00.000-04:00",
                            },
                            {
                                "value": "1210",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "1200",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:45:00.000-04:00",
                            },
                            {
                                "value": "1190",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "1190",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:15:00.000-04:00",
                            },
                            {
                                "value": "1180",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "1170",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:45:00.000-04:00",
                            },
                            {
                                "value": "1160",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "1150",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:15:00.000-04:00",
                            },
                            {
                                "value": "1150",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "1140",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:45:00.000-04:00",
                            },
                            {
                                "value": "1130",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "1130",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:15:00.000-04:00",
                            },
                            {
                                "value": "1120",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "1120",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:45:00.000-04:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "1100",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:15:00.000-04:00",
                            },
                            {
                                "value": "1090",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                            {
                                "value": "1090",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121813}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00060:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00065",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807202,
                            "default": True,
                        }
                    ],
                    "variableName": "Gage height, ft",
                    "variableDescription": "Gage height, feet",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807202",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "8.25",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "8.33",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:15:00.000-04:00",
                            },
                            {
                                "value": "8.40",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "8.47",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T00:45:00.000-04:00",
                            },
                            {
                                "value": "8.54",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "8.59",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:15:00.000-04:00",
                            },
                            {
                                "value": "8.63",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "8.63",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T01:45:00.000-04:00",
                            },
                            {
                                "value": "8.68",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "8.70",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:15:00.000-04:00",
                            },
                            {
                                "value": "8.71",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "8.70",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T02:45:00.000-04:00",
                            },
                            {
                                "value": "8.69",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "8.67",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:15:00.000-04:00",
                            },
                            {
                                "value": "8.65",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "8.63",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T03:45:00.000-04:00",
                            },
                            {
                                "value": "8.59",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "8.54",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:15:00.000-04:00",
                            },
                            {
                                "value": "8.54",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "8.46",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T04:45:00.000-04:00",
                            },
                            {
                                "value": "8.41",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "8.35",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:15:00.000-04:00",
                            },
                            {
                                "value": "8.30",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "8.24",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T05:45:00.000-04:00",
                            },
                            {
                                "value": "8.19",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "8.13",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:15:00.000-04:00",
                            },
                            {
                                "value": "8.09",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "8.03",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T06:45:00.000-04:00",
                            },
                            {
                                "value": "8.03",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "7.93",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:15:00.000-04:00",
                            },
                            {
                                "value": "7.88",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "7.83",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T07:45:00.000-04:00",
                            },
                            {
                                "value": "7.79",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "7.74",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:15:00.000-04:00",
                            },
                            {
                                "value": "7.70",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "7.66",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T08:45:00.000-04:00",
                            },
                            {
                                "value": "7.62",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "7.58",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:15:00.000-04:00",
                            },
                            {
                                "value": "7.55",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "7.51",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T09:45:00.000-04:00",
                            },
                            {
                                "value": "7.48",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "7.45",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:15:00.000-04:00",
                            },
                            {
                                "value": "7.42",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "7.39",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T10:45:00.000-04:00",
                            },
                            {
                                "value": "7.36",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "7.33",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:15:00.000-04:00",
                            },
                            {
                                "value": "7.32",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "7.29",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T11:45:00.000-04:00",
                            },
                            {
                                "value": "7.27",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "7.25",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:15:00.000-04:00",
                            },
                            {
                                "value": "7.22",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "7.20",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T12:45:00.000-04:00",
                            },
                            {
                                "value": "7.19",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "7.17",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:15:00.000-04:00",
                            },
                            {
                                "value": "7.15",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "7.13",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T13:45:00.000-04:00",
                            },
                            {
                                "value": "7.12",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "7.10",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:15:00.000-04:00",
                            },
                            {
                                "value": "7.08",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "7.07",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T14:45:00.000-04:00",
                            },
                            {
                                "value": "7.05",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "7.04",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:15:00.000-04:00",
                            },
                            {
                                "value": "7.02",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "7.01",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T15:45:00.000-04:00",
                            },
                            {
                                "value": "6.99",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "6.98",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:15:00.000-04:00",
                            },
                            {
                                "value": "6.97",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "6.96",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T16:45:00.000-04:00",
                            },
                            {
                                "value": "6.94",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "6.93",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:15:00.000-04:00",
                            },
                            {
                                "value": "6.92",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "6.91",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T17:45:00.000-04:00",
                            },
                            {
                                "value": "6.90",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "6.88",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:15:00.000-04:00",
                            },
                            {
                                "value": "6.88",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "6.86",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T18:45:00.000-04:00",
                            },
                            {
                                "value": "6.85",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "6.84",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:15:00.000-04:00",
                            },
                            {
                                "value": "6.83",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "6.82",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T19:45:00.000-04:00",
                            },
                            {
                                "value": "6.81",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "6.80",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:15:00.000-04:00",
                            },
                            {
                                "value": "6.79",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "6.78",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T20:45:00.000-04:00",
                            },
                            {
                                "value": "6.77",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "6.76",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:15:00.000-04:00",
                            },
                            {
                                "value": "6.75",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "6.74",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T21:45:00.000-04:00",
                            },
                            {
                                "value": "6.73",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "6.73",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:15:00.000-04:00",
                            },
                            {
                                "value": "6.72",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "6.71",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T22:45:00.000-04:00",
                            },
                            {
                                "value": "6.70",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "6.69",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:15:00.000-04:00",
                            },
                            {
                                "value": "6.68",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                            {
                                "value": "6.67",
                                "qualifiers": ["P"],
                                "dateTime": "2018-06-01T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121814}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00065:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00010",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807042,
                            "default": True,
                        }
                    ],
                    "variableName": "Temperature, water, &#176;C",
                    "variableDescription": "Temperature, water, degrees Celsius",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "deg C"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807042",
                },
                "values": [
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122067}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                    {
                        "value": [
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:15:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:45:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:15:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:45:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:15:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:45:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:15:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:45:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:15:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:45:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:15:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:45:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:15:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:45:00.000-04:00",
                            },
                            {
                                "value": "21.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:15:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "22.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:45:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:15:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "22.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:45:00.000-04:00",
                            },
                            {
                                "value": "22.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "22.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:15:00.000-04:00",
                            },
                            {
                                "value": "22.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "22.3",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:45:00.000-04:00",
                            },
                            {
                                "value": "22.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "22.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:15:00.000-04:00",
                            },
                            {
                                "value": "22.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "22.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:45:00.000-04:00",
                            },
                            {
                                "value": "22.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "22.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:15:00.000-04:00",
                            },
                            {
                                "value": "22.8",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "22.8",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:45:00.000-04:00",
                            },
                            {
                                "value": "22.8",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "22.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:15:00.000-04:00",
                            },
                            {
                                "value": "23.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "23.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:45:00.000-04:00",
                            },
                            {
                                "value": "23.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "23.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:15:00.000-04:00",
                            },
                            {
                                "value": "23.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "23.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:45:00.000-04:00",
                            },
                            {
                                "value": "23.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "23.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:15:00.000-04:00",
                            },
                            {
                                "value": "23.8",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "23.8",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:45:00.000-04:00",
                            },
                            {
                                "value": "23.9",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "24.0",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:15:00.000-04:00",
                            },
                            {
                                "value": "24.1",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "24.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:45:00.000-04:00",
                            },
                            {
                                "value": "24.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "24.2",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:15:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:45:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:15:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:45:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:15:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:45:00.000-04:00",
                            },
                            {
                                "value": "24.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "24.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:15:00.000-04:00",
                            },
                            {
                                "value": "24.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "24.7",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:45:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:15:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:45:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:15:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "24.6",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:45:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:15:00.000-04:00",
                            },
                            {
                                "value": "24.5",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:45:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:15:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                            {
                                "value": "24.4",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [
                            {"methodDescription": "WALNUT ST PIER", "methodID": 122073}
                        ],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                ],
                "name": "USGS:01570500:00010:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00045",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807140,
                            "default": True,
                        }
                    ],
                    "variableName": "Precipitation, total, in",
                    "variableDescription": "Precipitation, total, inches",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "in"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807140",
                },
                "values": [
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122072}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01570500:00045:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "42200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "42200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "42200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "42700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "42700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "42700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "42700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "42700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "42400",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "42200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "41900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "41700",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "41500",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "41000",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "40800",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "40500",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "40300",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "40100",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "39900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "39600",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "39600",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "39400",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "39400",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "39200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "39000",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "39000",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "38800",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "38500",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "38500",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "38300",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "38300",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "38100",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "38100",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "37800",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "37600",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "37600",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "37400",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "37400",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "37200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "36900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "36900",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122065}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01570500:00060:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00065",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807202,
                            "default": True,
                        }
                    ],
                    "variableName": "Gage height, ft",
                    "variableDescription": "Gage height, feet",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807202",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "5.25",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "5.25",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "5.25",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "5.27",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "5.27",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "5.27",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "5.27",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "5.27",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "5.26",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "5.25",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "5.24",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "5.23",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "5.22",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "5.20",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "5.19",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "5.18",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "5.17",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "5.16",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "5.15",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "5.14",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "5.14",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "5.13",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "5.13",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "5.12",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "5.11",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "5.11",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "5.10",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "5.09",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "5.09",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "5.08",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "5.08",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "5.07",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "5.07",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "5.06",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "5.05",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "5.05",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "5.04",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "5.04",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "5.03",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "5.02",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "5.02",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122066}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01570500:00065:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00095",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807295,
                            "default": True,
                        }
                    ],
                    "variableName": "Specific conductance, water, unfiltered, microsiemens per centimeter at 25&#176;C",
                    "variableDescription": "Specific conductance, water, unfiltered, microsiemens per centimeter at 25 degrees Celsius",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "uS/cm @25C"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807295",
                },
                "values": [
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122068}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                    {
                        "value": [
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:00:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:15:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:30:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T00:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T01:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T02:45:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T03:45:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:30:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T04:45:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:00:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:15:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:30:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T05:45:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:00:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:30:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T06:45:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:00:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:30:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T07:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T08:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T09:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T10:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T11:45:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:00:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T12:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:00:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:15:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:30:00.000-04:00",
                            },
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T13:45:00.000-04:00",
                            },
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:00:00.000-04:00",
                            },
                            {
                                "value": "195",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:15:00.000-04:00",
                            },
                            {
                                "value": "195",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:30:00.000-04:00",
                            },
                            {
                                "value": "195",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T14:45:00.000-04:00",
                            },
                            {
                                "value": "195",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:00:00.000-04:00",
                            },
                            {
                                "value": "195",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:15:00.000-04:00",
                            },
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:30:00.000-04:00",
                            },
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T15:45:00.000-04:00",
                            },
                            {
                                "value": "196",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:00:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:15:00.000-04:00",
                            },
                            {
                                "value": "197",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T16:45:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:00:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:30:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T17:45:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:00:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:15:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:30:00.000-04:00",
                            },
                            {
                                "value": "198",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T18:45:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:00:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:30:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T19:45:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:00:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:15:00.000-04:00",
                            },
                            {
                                "value": "199",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:30:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T20:45:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:00:00.000-04:00",
                            },
                            {
                                "value": "201",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:15:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:30:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T21:45:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:00:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:15:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:30:00.000-04:00",
                            },
                            {
                                "value": "201",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T22:45:00.000-04:00",
                            },
                            {
                                "value": "201",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:00:00.000-04:00",
                            },
                            {
                                "value": "201",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:15:00.000-04:00",
                            },
                            {
                                "value": "200",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:30:00.000-04:00",
                            },
                            {
                                "value": "201",
                                "qualifiers": ["A"],
                                "dateTime": "2018-06-01T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [
                            {"methodDescription": "WALNUT ST PIER", "methodID": 122074}
                        ],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                ],
                "name": "USGS:01570500:00095:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00300",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45809894,
                            "default": True,
                        }
                    ],
                    "variableName": "Dissolved oxygen, water, unfiltered, mg/L",
                    "variableDescription": "Dissolved oxygen, water, unfiltered, milligrams per liter",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "mg/l"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45809894",
                },
                "values": [
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122069}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [
                            {"methodDescription": "WALNUT ST PIER", "methodID": 122076}
                        ],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                ],
                "name": "USGS:01570500:00300:00000",
            },
            {
                "sourceInfo": {
                    "siteName": "Susquehanna River at Harrisburg, PA",
                    "siteCode": [
                        {"value": "01570500", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.25481164,
                            "longitude": -76.8860846,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050305", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42043", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00400",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45810855,
                            "default": True,
                        }
                    ],
                    "variableName": "pH, water, unfiltered, field, standard units",
                    "variableDescription": "pH, water, unfiltered, field, standard units",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "std units"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45810855",
                },
                "values": [
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 122070}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                    {
                        "value": [],
                        "qualifier": [],
                        "qualityControlLevel": [],
                        "method": [
                            {"methodDescription": "WALNUT ST PIER", "methodID": 122075}
                        ],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    },
                ],
                "name": "USGS:01570500:00400:00000",
            },
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}


# XXX: flag for start of startDST dict.

startDST = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://nwis.waterservices.usgs.gov/nwis/iv/format=json&sites=01541000&startDT=2018-03-10&endDT=2018-03-12&parameterCd=00060",
            "criteria": {
                "locationParam": "[ALL:01541000]",
                "variableParam": "[00060]",
                "timeParam": {
                    "beginDateTime": "2018-03-10T00:00:00.000",
                    "endDateTime": "2018-03-12T23:59:59.000",
                },
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01541000]", "title": "filter:sites"},
                {
                    "value": "[mode=RANGE, modifiedSince=null] interval={INTERVAL[2018-03-10T00:00:00.000-05:00/2018-03-12T23:59:59.000Z]}",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-25T03:17:14.367Z", "title": "requestDT"},
                {"value": "d90e31e0-38ab-11e9-a754-3440b59d3362", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "nadww02", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "668",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T00:00:00.000-05:00",
                            },
                            {
                                "value": "668",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T00:15:00.000-05:00",
                            },
                            {
                                "value": "668",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T00:30:00.000-05:00",
                            },
                            {
                                "value": "668",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T00:45:00.000-05:00",
                            },
                            {
                                "value": "668",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T01:00:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T01:15:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T01:30:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T01:45:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T02:00:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T02:15:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T02:30:00.000-05:00",
                            },
                            {
                                "value": "662",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T02:45:00.000-05:00",
                            },
                            {
                                "value": "657",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T03:00:00.000-05:00",
                            },
                            {
                                "value": "657",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T03:15:00.000-05:00",
                            },
                            {
                                "value": "657",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T03:30:00.000-05:00",
                            },
                            {
                                "value": "657",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T03:45:00.000-05:00",
                            },
                            {
                                "value": "657",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T04:00:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T04:15:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T04:30:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T04:45:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T05:00:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T05:15:00.000-05:00",
                            },
                            {
                                "value": "651",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T05:30:00.000-05:00",
                            },
                            {
                                "value": "645",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T05:45:00.000-05:00",
                            },
                            {
                                "value": "645",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T06:00:00.000-05:00",
                            },
                            {
                                "value": "645",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T06:15:00.000-05:00",
                            },
                            {
                                "value": "645",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T06:30:00.000-05:00",
                            },
                            {
                                "value": "645",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T06:45:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T07:00:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T07:15:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T07:30:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T07:45:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T08:00:00.000-05:00",
                            },
                            {
                                "value": "640",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T08:15:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T08:30:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T08:45:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T09:00:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T09:15:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T09:30:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T09:45:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T10:00:00.000-05:00",
                            },
                            {
                                "value": "634",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T10:15:00.000-05:00",
                            },
                            {
                                "value": "629",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T10:30:00.000-05:00",
                            },
                            {
                                "value": "629",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T10:45:00.000-05:00",
                            },
                            {
                                "value": "629",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T11:00:00.000-05:00",
                            },
                            {
                                "value": "629",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T11:15:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T11:30:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T11:45:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T12:00:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T12:15:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T12:30:00.000-05:00",
                            },
                            {
                                "value": "624",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T12:45:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T13:00:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T13:15:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T13:30:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T13:45:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T14:00:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T14:15:00.000-05:00",
                            },
                            {
                                "value": "618",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T14:30:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T14:45:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T15:00:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T15:15:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T15:30:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T15:45:00.000-05:00",
                            },
                            {
                                "value": "613",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T16:00:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T16:15:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T16:30:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T16:45:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T17:00:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T17:15:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T17:30:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T17:45:00.000-05:00",
                            },
                            {
                                "value": "607",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T18:00:00.000-05:00",
                            },
                            {
                                "value": "602",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T18:15:00.000-05:00",
                            },
                            {
                                "value": "602",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T18:30:00.000-05:00",
                            },
                            {
                                "value": "602",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T18:45:00.000-05:00",
                            },
                            {
                                "value": "602",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T19:00:00.000-05:00",
                            },
                            {
                                "value": "602",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T19:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T19:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T19:45:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T20:00:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T20:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T20:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T20:45:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T21:00:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T21:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T21:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T21:45:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T22:00:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T22:15:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T22:30:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T22:45:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T23:00:00.000-05:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T23:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T23:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-10T23:45:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T00:00:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T00:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T00:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T00:45:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T01:00:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T01:15:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T01:30:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T01:45:00.000-05:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T03:00:00.000-04:00",
                            },
                            {
                                "value": "597",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T03:15:00.000-04:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T03:30:00.000-04:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T03:45:00.000-04:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T04:00:00.000-04:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T04:15:00.000-04:00",
                            },
                            {
                                "value": "592",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T04:30:00.000-04:00",
                            },
                            {
                                "value": "586",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T04:45:00.000-04:00",
                            },
                            {
                                "value": "586",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T05:00:00.000-04:00",
                            },
                            {
                                "value": "586",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T05:15:00.000-04:00",
                            },
                            {
                                "value": "581",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T05:30:00.000-04:00",
                            },
                            {
                                "value": "581",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T05:45:00.000-04:00",
                            },
                            {
                                "value": "581",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T06:00:00.000-04:00",
                            },
                            {
                                "value": "581",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T06:15:00.000-04:00",
                            },
                            {
                                "value": "581",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T06:30:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T06:45:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T07:00:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T07:15:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T07:30:00.000-04:00",
                            },
                            {
                                "value": "571",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T07:45:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T08:00:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T08:15:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T08:30:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T08:45:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T09:00:00.000-04:00",
                            },
                            {
                                "value": "571",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T09:15:00.000-04:00",
                            },
                            {
                                "value": "571",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T09:30:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T09:45:00.000-04:00",
                            },
                            {
                                "value": "576",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T10:00:00.000-04:00",
                            },
                            {
                                "value": "571",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T10:15:00.000-04:00",
                            },
                            {
                                "value": "571",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T10:30:00.000-04:00",
                            },
                            {
                                "value": "566",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T10:45:00.000-04:00",
                            },
                            {
                                "value": "566",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T11:00:00.000-04:00",
                            },
                            {
                                "value": "566",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T11:15:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T11:30:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T11:45:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T12:00:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T12:15:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T12:30:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T12:45:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T13:00:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T13:15:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T13:30:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T13:45:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T14:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T14:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T14:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T14:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T15:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T15:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T15:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T15:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T16:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T16:15:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T16:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T16:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T17:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T17:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T17:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T17:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T18:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T18:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T18:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T18:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T19:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T19:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T19:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T19:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T20:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T20:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T20:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T20:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T21:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T21:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T21:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T21:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T22:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T22:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T22:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T22:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T23:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T23:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T23:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-11T23:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T00:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T00:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T00:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T00:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T01:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T01:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T01:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T01:45:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T02:00:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T02:15:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T02:30:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T02:45:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T03:00:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T03:15:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T03:30:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T03:45:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T04:00:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T04:15:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T04:30:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T04:45:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T05:00:00.000-04:00",
                            },
                            {
                                "value": "561",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T05:15:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T05:30:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T05:45:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T06:00:00.000-04:00",
                            },
                            {
                                "value": "556",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T06:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T06:30:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T06:45:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T07:00:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T07:15:00.000-04:00",
                            },
                            {
                                "value": "551",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T07:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T07:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T08:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T08:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T08:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T08:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T09:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T09:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T09:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T09:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T10:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T10:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T10:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T10:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T11:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T11:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T11:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T11:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T12:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T12:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T12:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T12:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T13:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T13:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T13:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T13:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T14:00:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T14:15:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T14:30:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T14:45:00.000-04:00",
                            },
                            {
                                "value": "546",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T15:00:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T15:15:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T15:30:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T15:45:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T16:00:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T16:15:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T16:30:00.000-04:00",
                            },
                            {
                                "value": "541",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T16:45:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T17:00:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T17:15:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T17:30:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T17:45:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T18:00:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T18:15:00.000-04:00",
                            },
                            {
                                "value": "536",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T18:30:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T18:45:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T19:00:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T19:15:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T19:30:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T19:45:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T20:00:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T20:15:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T20:30:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T20:45:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T21:00:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T21:15:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T21:30:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T21:45:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T22:00:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T22:15:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T22:30:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T22:45:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T23:00:00.000-04:00",
                            },
                            {
                                "value": "531",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T23:15:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T23:30:00.000-04:00",
                            },
                            {
                                "value": "526",
                                "qualifiers": ["A"],
                                "dateTime": "2018-03-12T23:45:00.000-04:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "A",
                                "qualifierDescription": "Approved for publication -- Processing and review completed.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121813}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00060:00000",
            }
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}


# XXX: flag for start of endDST dict.

endDST = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://waterservices.usgs.gov/nwis/iv/format=json&sites=01541000&startDT=2018-11-03&endDT=2018-11-05&parameterCd=00060",
            "criteria": {
                "locationParam": "[ALL:01541000]",
                "variableParam": "[00060]",
                "timeParam": {
                    "beginDateTime": "2018-11-03T00:00:00.000",
                    "endDateTime": "2018-11-05T23:59:59.000",
                },
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01541000]", "title": "filter:sites"},
                {
                    "value": "[mode=RANGE, modifiedSince=null] interval={INTERVAL[2018-11-03T00:00:00.000-04:00/2018-11-05T23:59:59.000Z]}",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-02-25T03:17:14.970Z", "title": "requestDT"},
                {"value": "d96a3490-38ab-11e9-9463-6cae8b6642f6", "title": "requestId"},
                {
                    "value": "Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.",
                    "title": "disclaimer",
                },
                {"value": "caas01", "title": "server"},
            ],
        },
        "timeSeries": [
            {
                "sourceInfo": {
                    "siteName": "West Branch Susquehanna River at Bower, PA",
                    "siteCode": [
                        {"value": "01541000", "network": "NWIS", "agencyCode": "USGS"}
                    ],
                    "timeZoneInfo": {
                        "defaultTimeZone": {
                            "zoneOffset": "-05:00",
                            "zoneAbbreviation": "EST",
                        },
                        "daylightSavingsTimeZone": {
                            "zoneOffset": "-04:00",
                            "zoneAbbreviation": "EDT",
                        },
                        "siteUsesDaylightSavingsTime": True,
                    },
                    "geoLocation": {
                        "geogLocation": {
                            "srs": "EPSG:4326",
                            "latitude": 40.89700655,
                            "longitude": -78.6769726,
                        },
                        "localSiteXY": [],
                    },
                    "note": [],
                    "siteType": [],
                    "siteProperty": [
                        {"value": "ST", "name": "siteTypeCd"},
                        {"value": "02050201", "name": "hucCd"},
                        {"value": "42", "name": "stateCd"},
                        {"value": "42033", "name": "countyCd"},
                    ],
                },
                "variable": {
                    "variableCode": [
                        {
                            "value": "00060",
                            "network": "NWIS",
                            "vocabulary": "NWIS:UnitValues",
                            "variableID": 45807197,
                            "default": True,
                        }
                    ],
                    "variableName": "Streamflow, ft&#179;/s",
                    "variableDescription": "Discharge, cubic feet per second",
                    "valueType": "Derived Value",
                    "unit": {"unitCode": "ft3/s"},
                    "options": {
                        "option": [{"name": "Statistic", "optionCode": "00000"}]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807197",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "1000",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T00:00:00.000-04:00",
                            },
                            {
                                "value": "994",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T00:15:00.000-04:00",
                            },
                            {
                                "value": "994",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T00:30:00.000-04:00",
                            },
                            {
                                "value": "987",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T00:45:00.000-04:00",
                            },
                            {
                                "value": "987",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T01:00:00.000-04:00",
                            },
                            {
                                "value": "980",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T01:15:00.000-04:00",
                            },
                            {
                                "value": "980",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T01:30:00.000-04:00",
                            },
                            {
                                "value": "980",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T01:45:00.000-04:00",
                            },
                            {
                                "value": "980",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T02:00:00.000-04:00",
                            },
                            {
                                "value": "974",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T02:15:00.000-04:00",
                            },
                            {
                                "value": "974",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T02:30:00.000-04:00",
                            },
                            {
                                "value": "974",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T02:45:00.000-04:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T03:00:00.000-04:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T03:15:00.000-04:00",
                            },
                            {
                                "value": "967",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T03:30:00.000-04:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T03:45:00.000-04:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T04:00:00.000-04:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T04:15:00.000-04:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T04:30:00.000-04:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T04:45:00.000-04:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T05:00:00.000-04:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T05:15:00.000-04:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T05:30:00.000-04:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T05:45:00.000-04:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T06:00:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T06:15:00.000-04:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T06:30:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T06:45:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T07:00:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T07:15:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T07:30:00.000-04:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T07:45:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T08:00:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T08:15:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T08:30:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T08:45:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T09:00:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T09:15:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T09:30:00.000-04:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T09:45:00.000-04:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T10:00:00.000-04:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T10:15:00.000-04:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T10:30:00.000-04:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T10:45:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T11:00:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T11:15:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T11:30:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T11:45:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T12:00:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T12:15:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T12:30:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T12:45:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T13:00:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T13:15:00.000-04:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T13:30:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T13:45:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T14:00:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T14:15:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T14:30:00.000-04:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T14:45:00.000-04:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T15:00:00.000-04:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T15:15:00.000-04:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T15:30:00.000-04:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T15:45:00.000-04:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T16:00:00.000-04:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T16:15:00.000-04:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T16:30:00.000-04:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T16:45:00.000-04:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T17:00:00.000-04:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T17:15:00.000-04:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T17:30:00.000-04:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T17:45:00.000-04:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T18:00:00.000-04:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T18:15:00.000-04:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T18:30:00.000-04:00",
                            },
                            {
                                "value": "890",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T18:45:00.000-04:00",
                            },
                            {
                                "value": "890",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T19:00:00.000-04:00",
                            },
                            {
                                "value": "890",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T19:15:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T19:30:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T19:45:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T20:00:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T20:15:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T20:30:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T20:45:00.000-04:00",
                            },
                            {
                                "value": "883",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T21:00:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T21:15:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T21:30:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T21:45:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T22:00:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T22:15:00.000-04:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T22:30:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T22:45:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T23:00:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T23:15:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T23:30:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-03T23:45:00.000-04:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T00:00:00.000-04:00",
                            },
                            {
                                "value": "865",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T00:15:00.000-04:00",
                            },
                            {
                                "value": "865",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T00:30:00.000-04:00",
                            },
                            {
                                "value": "865",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T00:45:00.000-04:00",
                            },
                            {
                                "value": "865",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:00:00.000-04:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:15:00.000-04:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:30:00.000-04:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:45:00.000-04:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:00:00.000-05:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:15:00.000-05:00",
                            },
                            {
                                "value": "852",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:30:00.000-05:00",
                            },
                            {
                                "value": "852",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T01:45:00.000-05:00",
                            },
                            {
                                "value": "852",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T02:00:00.000-05:00",
                            },
                            {
                                "value": "852",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T02:15:00.000-05:00",
                            },
                            {
                                "value": "846",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T02:30:00.000-05:00",
                            },
                            {
                                "value": "846",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T02:45:00.000-05:00",
                            },
                            {
                                "value": "846",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T03:00:00.000-05:00",
                            },
                            {
                                "value": "846",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T03:15:00.000-05:00",
                            },
                            {
                                "value": "840",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T03:30:00.000-05:00",
                            },
                            {
                                "value": "840",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T03:45:00.000-05:00",
                            },
                            {
                                "value": "840",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T04:00:00.000-05:00",
                            },
                            {
                                "value": "840",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T04:15:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T04:30:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T04:45:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T05:00:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T05:15:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T05:30:00.000-05:00",
                            },
                            {
                                "value": "828",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T05:45:00.000-05:00",
                            },
                            {
                                "value": "828",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T06:00:00.000-05:00",
                            },
                            {
                                "value": "828",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T06:15:00.000-05:00",
                            },
                            {
                                "value": "822",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T06:30:00.000-05:00",
                            },
                            {
                                "value": "822",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T06:45:00.000-05:00",
                            },
                            {
                                "value": "822",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T07:00:00.000-05:00",
                            },
                            {
                                "value": "822",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T07:15:00.000-05:00",
                            },
                            {
                                "value": "816",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T07:30:00.000-05:00",
                            },
                            {
                                "value": "816",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T07:45:00.000-05:00",
                            },
                            {
                                "value": "816",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T08:00:00.000-05:00",
                            },
                            {
                                "value": "810",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T08:15:00.000-05:00",
                            },
                            {
                                "value": "810",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T08:30:00.000-05:00",
                            },
                            {
                                "value": "810",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T08:45:00.000-05:00",
                            },
                            {
                                "value": "804",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T09:00:00.000-05:00",
                            },
                            {
                                "value": "804",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T09:15:00.000-05:00",
                            },
                            {
                                "value": "804",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T09:30:00.000-05:00",
                            },
                            {
                                "value": "804",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T09:45:00.000-05:00",
                            },
                            {
                                "value": "798",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T10:00:00.000-05:00",
                            },
                            {
                                "value": "798",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T10:15:00.000-05:00",
                            },
                            {
                                "value": "798",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T10:30:00.000-05:00",
                            },
                            {
                                "value": "792",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T10:45:00.000-05:00",
                            },
                            {
                                "value": "792",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T11:00:00.000-05:00",
                            },
                            {
                                "value": "792",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T11:15:00.000-05:00",
                            },
                            {
                                "value": "792",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T11:30:00.000-05:00",
                            },
                            {
                                "value": "787",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T11:45:00.000-05:00",
                            },
                            {
                                "value": "787",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T12:00:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T12:15:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T12:30:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T12:45:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T13:00:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T13:15:00.000-05:00",
                            },
                            {
                                "value": "775",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T13:30:00.000-05:00",
                            },
                            {
                                "value": "775",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T13:45:00.000-05:00",
                            },
                            {
                                "value": "775",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T14:00:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T14:15:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T14:30:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T14:45:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T15:00:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T15:15:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T15:30:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T15:45:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T16:00:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T16:15:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T16:30:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T16:45:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T17:00:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T17:15:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T17:30:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T17:45:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T18:00:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T18:15:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T18:30:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T18:45:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T19:00:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T19:15:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T19:30:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T19:45:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T20:00:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T20:15:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T20:30:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T20:45:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T21:00:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T21:15:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T21:30:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T21:45:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T22:00:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T22:15:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T22:30:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T22:45:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T23:00:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T23:15:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T23:30:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-04T23:45:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T00:00:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T00:15:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T00:30:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T00:45:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T01:00:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T01:15:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T01:30:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T01:45:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T02:00:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T02:15:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T02:30:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T02:45:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T03:00:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T03:15:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T03:30:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T03:45:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T04:00:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T04:15:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T04:30:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T04:45:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T05:00:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T05:15:00.000-05:00",
                            },
                            {
                                "value": "713",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T05:30:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T05:45:00.000-05:00",
                            },
                            {
                                "value": "718",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T06:00:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T06:15:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T06:30:00.000-05:00",
                            },
                            {
                                "value": "724",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T06:45:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T07:00:00.000-05:00",
                            },
                            {
                                "value": "729",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T07:15:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T07:30:00.000-05:00",
                            },
                            {
                                "value": "735",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T07:45:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T08:00:00.000-05:00",
                            },
                            {
                                "value": "741",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T08:15:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T08:30:00.000-05:00",
                            },
                            {
                                "value": "746",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T08:45:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T09:00:00.000-05:00",
                            },
                            {
                                "value": "752",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T09:15:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T09:30:00.000-05:00",
                            },
                            {
                                "value": "758",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T09:45:00.000-05:00",
                            },
                            {
                                "value": "763",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T10:00:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T10:15:00.000-05:00",
                            },
                            {
                                "value": "769",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T10:30:00.000-05:00",
                            },
                            {
                                "value": "775",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T10:45:00.000-05:00",
                            },
                            {
                                "value": "781",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T11:00:00.000-05:00",
                            },
                            {
                                "value": "787",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T11:15:00.000-05:00",
                            },
                            {
                                "value": "792",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T11:30:00.000-05:00",
                            },
                            {
                                "value": "798",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T11:45:00.000-05:00",
                            },
                            {
                                "value": "804",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T12:00:00.000-05:00",
                            },
                            {
                                "value": "810",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T12:15:00.000-05:00",
                            },
                            {
                                "value": "816",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T12:30:00.000-05:00",
                            },
                            {
                                "value": "822",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T12:45:00.000-05:00",
                            },
                            {
                                "value": "828",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T13:00:00.000-05:00",
                            },
                            {
                                "value": "834",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T13:15:00.000-05:00",
                            },
                            {
                                "value": "846",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T13:30:00.000-05:00",
                            },
                            {
                                "value": "852",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T13:45:00.000-05:00",
                            },
                            {
                                "value": "858",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T14:00:00.000-05:00",
                            },
                            {
                                "value": "865",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T14:15:00.000-05:00",
                            },
                            {
                                "value": "871",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T14:30:00.000-05:00",
                            },
                            {
                                "value": "877",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T14:45:00.000-05:00",
                            },
                            {
                                "value": "890",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T15:00:00.000-05:00",
                            },
                            {
                                "value": "896",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T15:15:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T15:30:00.000-05:00",
                            },
                            {
                                "value": "902",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T15:45:00.000-05:00",
                            },
                            {
                                "value": "909",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T16:00:00.000-05:00",
                            },
                            {
                                "value": "915",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T16:15:00.000-05:00",
                            },
                            {
                                "value": "921",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T16:30:00.000-05:00",
                            },
                            {
                                "value": "928",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T16:45:00.000-05:00",
                            },
                            {
                                "value": "934",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T17:00:00.000-05:00",
                            },
                            {
                                "value": "941",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T17:15:00.000-05:00",
                            },
                            {
                                "value": "947",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T17:30:00.000-05:00",
                            },
                            {
                                "value": "954",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T17:45:00.000-05:00",
                            },
                            {
                                "value": "960",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T18:00:00.000-05:00",
                            },
                            {
                                "value": "974",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T18:15:00.000-05:00",
                            },
                            {
                                "value": "980",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T18:30:00.000-05:00",
                            },
                            {
                                "value": "987",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T18:45:00.000-05:00",
                            },
                            {
                                "value": "1000",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T19:00:00.000-05:00",
                            },
                            {
                                "value": "1010",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T19:15:00.000-05:00",
                            },
                            {
                                "value": "1020",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T19:30:00.000-05:00",
                            },
                            {
                                "value": "1030",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T19:45:00.000-05:00",
                            },
                            {
                                "value": "1040",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T20:00:00.000-05:00",
                            },
                            {
                                "value": "1060",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T20:15:00.000-05:00",
                            },
                            {
                                "value": "1060",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T20:30:00.000-05:00",
                            },
                            {
                                "value": "1080",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T20:45:00.000-05:00",
                            },
                            {
                                "value": "1080",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T21:00:00.000-05:00",
                            },
                            {
                                "value": "1090",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T21:15:00.000-05:00",
                            },
                            {
                                "value": "1100",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T21:30:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T21:45:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T22:00:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T22:15:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T22:30:00.000-05:00",
                            },
                            {
                                "value": "1120",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T22:45:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T23:00:00.000-05:00",
                            },
                            {
                                "value": "1120",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T23:15:00.000-05:00",
                            },
                            {
                                "value": "1120",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T23:30:00.000-05:00",
                            },
                            {
                                "value": "1110",
                                "qualifiers": ["P"],
                                "dateTime": "2018-11-05T23:45:00.000-05:00",
                            },
                        ],
                        "qualifier": [
                            {
                                "qualifierCode": "P",
                                "qualifierDescription": "Provisional data subject to revision.",
                                "qualifierID": 0,
                                "network": "NWIS",
                                "vocabulary": "uv_rmk_cd",
                            }
                        ],
                        "qualityControlLevel": [],
                        "method": [{"methodDescription": "", "methodID": 121813}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541000:00060:00000",
            }
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}
