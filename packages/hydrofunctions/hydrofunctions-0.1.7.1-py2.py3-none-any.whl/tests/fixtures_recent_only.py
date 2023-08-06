# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:24:48 2019

@author: Marty
"""
# hf.NWIS('01541200')
# https://waterservices.usgs.gov/nwis/dv/?format=json%2C1.1&sites=01541200

# This is a request that doesn't specify a starting date or a period, so NWIS
# returns the most recent readings.
# Amuseingly, for this site, that means you get a temperature reading from
# 1961 as well as discharge from today.
recent_only = {
    "name": "ns1:timeSeriesResponseType",
    "declaredType": "org.cuahsi.waterml.TimeSeriesResponseType",
    "scope": "javax.xml.bind.JAXBElement$GlobalScope",
    "value": {
        "queryInfo": {
            "queryURL": "http://waterservices.usgs.gov/nwis/dv/format=json%2C1.1&sites=01541200",
            "criteria": {
                "locationParam": "[ALL:01541200]",
                "variableParam": "ALL",
                "parameter": [],
            },
            "note": [
                {"value": "[ALL:01541200]", "title": "filter:sites"},
                {
                    "value": "[mode=LATEST, modifiedSince=null]",
                    "title": "filter:timeRange",
                },
                {"value": "methodIds=[ALL]", "title": "filter:methodId"},
                {"value": "2019-04-15T14:23:12.311Z", "title": "requestDT"},
                {"value": "00165560-5f8a-11e9-9824-6cae8b6642f6", "title": "requestId"},
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
                        "option": [
                            {
                                "value": "Random Instantaneous Values",
                                "name": "Statistic",
                                "optionCode": "00011",
                            }
                        ]
                    },
                    "note": [],
                    "noDataValue": -999999.0,
                    "variableProperty": [],
                    "oid": "45807042",
                },
                "values": [
                    {
                        "value": [
                            {
                                "value": "11.7",
                                "qualifiers": ["A"],
                                "dateTime": "1961-09-29T00:00:00.000",
                            }
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
                        "method": [{"methodDescription": "", "methodID": 118850}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541200:00010:00011",
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
                        "option": [
                            {
                                "value": "Mean",
                                "name": "Statistic",
                                "optionCode": "00003",
                            }
                        ]
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
                                "value": "717",
                                "qualifiers": ["P"],
                                "dateTime": "2019-04-14T00:00:00.000",
                            }
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
                        "method": [{"methodDescription": "", "methodID": 118849}],
                        "source": [],
                        "offset": [],
                        "sample": [],
                        "censorCode": [],
                    }
                ],
                "name": "USGS:01541200:00060:00003",
            },
        ],
    },
    "nil": False,
    "globalScope": True,
    "typeSubstituted": False,
}
