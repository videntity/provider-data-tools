#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars


AFFILIATION_PURPOSE = ('HIE-EXCHANGE', 'MEDICARE-NETWORK', 'MEDICAID-NETWORK',
                       'PRIVATE-PAYER-NETWORK', 'ACO-NETWORK', 'DOMAIN',
                       'PARENT-ORGANIZATION')

AFFILIATION_DATA_TYPE = ('NPI-1', 'NPI-2', 'HPID',
                         'OEID', 'MAC', 'EIN', 'PAC-ID', 'OTHER')

ENDPOINT_DATA_TYPE = (
    'DIRECT-EMAIL-ADDRESS',
    'REGULAR-EMAIL-ADDRESS',
    'SOAP-WS-URL',
    'CONNECT-URL',
    'FHIR-URL',
    'RESTFUL-WS-URL',
    'WEBSITE-URL',
    'OTHER-URL')


SUFFIX_CHOICES = ('Jr.', 'Sr.', 'I', 'II', 'III', 'IV',
                  'V', 'VI', 'VII', 'VIII', 'IX', 'X')

PREFIX_CHOICES = ('Ms.', 'Mr.', 'Miss', 'Mrs.', 'Dr.', 'Prof.')


INDIVIDUAL_OTHER_NAME_CHOICES = ("", "1", "2", "5")

SOLE_PROPRIETOR_OTHER_NAME_CHOICES = ("", "1", "2", "3", "5")

ORGANIZATION_OTHER_NAME_CHOICES = ("", "3", "4", "5")


OTHER_NAME_CHOICES = ("", "1", "2", "3", "4", "5")


LICENSE_TYPE_CODES = ('AK-APN', 'AK-CNA', 'AK-CNM', 'AK-CNS', 'AK-DCH', 'AK-DEN',
                      'AK-DOS', 'AK-DPM',
                      'AK-DVM', 'AK-MDR', 'AK-MWF', 'AK-NPR', 'AK-ODR', 'AK-PAS', 'AK-RPH', 'AK-UNK',
                      'AL-APN', 'AL-CNA', 'AL-CNM', 'AL-CNS', 'AL-DCH', 'AL-DEN', 'AL-DOS', 'AL-DPM',
                      'AL-DVM', 'AL-MDR', 'AL-MWF', 'AL-NPR', 'AL-ODR', 'AL-PAS', 'AL-RPH', 'AL-UNK',
                      'AR-APN', 'AR-CNA', 'AR-CNM', 'AR-CNS', 'AR-DCH', 'AR-DEN', 'AR-DOS', 'AR-DPM',
                      'AR-DVM', 'AR-MDR', 'AR-MWF', 'AR-NPR', 'AR-ODR', 'AR-PAS', 'AR-RPH', 'AR-UNK',
                      'AS-UNK', 'AZ-APN', 'AZ-CNA', 'AZ-CNM', 'AZ-CNS', 'AZ-DCH', 'AZ-DEN', 'AZ-DOS',
                      'AZ-DPM', 'AZ-DVM', 'AZ-MDR', 'AZ-MWF', 'AZ-NPR', 'AZ-ODR', 'AZ-PAS', 'AZ-RPH',
                      'AZ-UNK', 'CA-APN', 'CA-CNA', 'CA-CNM', 'CA-CNS', 'CA-DCH', 'CA-DEN', 'CA-DOS',
                      'CA-DPM', 'CA-DVM', 'CA-MDR', 'CA-MWF', 'CA-NPR', 'CA-ODR', 'CA-PAS', 'CA-RPH',
                      'CA-UNK', 'CO-APN', 'CO-CNA', 'CO-CNM', 'CO-CNS', 'CO-DCH', 'CO-DEN', 'CO-DOS',
                      'CO-DPM', 'CO-DVM', 'CO-MDR', 'CO-MDU', 'CO-MWF', 'CO-NPR', 'CO-ODR', 'CO-PAS',
                      'CO-RPH', 'CO-UNK', 'CT-APN', 'CT-CNA', 'CT-CNM', 'CT-CNS', 'CT-DCH', 'CT-DEN',
                      'CT-DOS', 'CT-DPM', 'CT-DVM', 'CT-MDR', 'CT-MWF', 'CT-NPR', 'CT-ODR', 'CT-PAS',
                      'CT-RPH', 'CT-UNK', 'DC-APN', 'DC-CNA', 'DC-CNM', 'DC-CNS', 'DC-DCH', 'DC-DEN',
                      'DC-DOS', 'DC-DPM', 'DC-DVM', 'DC-MDR', 'DC-MWF', 'DC-NPR', 'DC-ODR', 'DC-PAS',
                      'DC-RPH', 'DC-UNK', 'DE-APN', 'DE-CNA', 'DE-CNM', 'DE-CNS', 'DE-DCH', 'DE-DEN',
                      'DE-DOS', 'DE-DPM', 'DE-DVM', 'DE-MDR', 'DE-MWF', 'DE-NPR', 'DE-ODR', 'DE-PAS',
                      'DE-RPH', 'DE-UNK', 'FL-APN', 'FL-CNA', 'FL-CNM', 'FL-CNS', 'FL-DCH', 'FL-DEN',
                      'FL-DOS', 'FL-DPM', 'FL-DVM', 'FL-MDR', 'FL-MWF', 'FL-NPR', 'FL-ODR', 'FL-PAS',
                      'FL-RPH', 'FL-UNK', 'FM-UNK', 'GA-APN', 'GA-CNA', 'GA-CNM', 'GA-CNS', 'GA-DCH',
                      'GA-DEN', 'GA-DOS', 'GA-DPM', 'GA-DVM', 'GA-MDR', 'GA-MWF', 'GA-NPR', 'GA-ODR',
                      'GA-PAS', 'GA-RPH', 'GA-UNK', 'GU-UNK', 'HI-APN', 'HI-CNA', 'HI-CNM', 'HI-CNS',
                      'HI-DCH', 'HI-DEN', 'HI-DOS', 'HI-DPM', 'HI-DVM', 'HI-MDR', 'HI-MWF', 'HI-NPR',
                      'HI-ODR', 'HI-PAS', 'HI-RPH', 'HI-UNK', 'IA-APN', 'IA-CNA', 'IA-CNM', 'IA-CNS',
                      'IA-DCH', 'IA-DEN', 'IA-DOS', 'IA-DPM', 'IA-DVM', 'IA-MDR', 'IA-MWF', 'IA-NPR',
                      'IA-ODR', 'IA-PAS', 'IA-RPH', 'IA-UNK', 'ID-APN', 'ID-CNA', 'ID-CNM', 'ID-CNS',
                      'ID-DCH', 'ID-DEN', 'ID-DOS', 'ID-DPM', 'ID-DVM', 'ID-MDR', 'ID-MWF', 'ID-NPR',
                      'ID-ODR', 'ID-PAS', 'ID-RPH', 'ID-UNK', 'IL-APN', 'IL-CNA', 'IL-CNM', 'IL-CNS',
                      'IL-DCH', 'IL-DEN', 'IL-DOS', 'IL-DPM', 'IL-DVM', 'IL-MDR', 'IL-MWF', 'IL-NPR',
                      'IL-ODR', 'IL-PAS', 'IL-RPH', 'IL-UNK', 'IN-APN', 'IN-CNA', 'IN-CNM', 'IN-CNS',
                      'IN-DCH', 'IN-DEN', 'IN-DOS', 'IN-DPM', 'IN-DVM', 'IN-MDR', 'IN-MWF', 'IN-NPR',
                      'IN-ODR', 'IN-PAS', 'IN-RPH', 'IN-UNK', 'KS-APN', 'KS-CNA', 'KS-CNM', 'KS-CNS',
                      'KS-DCH', 'KS-DEN', 'KS-DOS', 'KS-DPM', 'KS-DVM', 'KS-MDR', 'KS-MWF', 'KS-NPR',
                      'KS-ODR', 'KS-PAS', 'KS-RPH', 'KS-UNK', 'KY-APN', 'KY-CNA', 'KY-CNM', 'KY-CNS',
                      'KY-DCH', 'KY-DEN', 'KY-DOS', 'KY-DPM', 'KY-DVM', 'KY-MDR', 'KY-MWF', 'KY-NPR',
                      'KY-ODR', 'KY-PAS', 'KY-RPH', 'KY-UNK', 'LA-APN', 'LA-CNA', 'LA-CNM', 'LA-CNS',
                      'LA-DCH', 'LA-DEN', 'LA-DOS', 'LA-DPM', 'LA-DVM', 'LA-MDR', 'LA-MWF', 'LA-NPR',
                      'LA-ODR', 'LA-PAS', 'LA-RPH', 'LA-UNK', 'MA-APN', 'MA-CNA', 'MA-CNM', 'MA-CNS',
                      'MA-DCH', 'MA-DEN', 'MA-DOS', 'MA-DPM', 'MA-DVM', 'MA-MDR', 'MA-MWF', 'MA-NPR',
                      'MA-ODR', 'MA-PAS', 'MA-RPH', 'MA-UNK', 'MD-APN', 'MD-CNA', 'MD-CNM', 'MD-CNS',
                      'MD-DCH', 'MD-DEN', 'MD-DOS', 'MD-DPM', 'MD-DVM', 'MD-MDR', 'MD-MWF', 'MD-NPR',
                      'MD-ODR', 'MD-PAS', 'MD-RPH', 'MD-UNK', 'ME-APN', 'ME-CNA', 'ME-CNM', 'ME-CNS',
                      'ME-DCH', 'ME-DEN', 'ME-DOS', 'ME-DPM', 'ME-DVM', 'ME-MDR', 'ME-MWF', 'ME-NPR',
                      'ME-ODR', 'ME-PAS', 'ME-RPH', 'ME-UNK', 'MH-UNK', 'MI-APN', 'MI-CNA', 'MI-CNM',
                      'MI-NPR', 'MI-ODR', 'MI-PAS', 'MI-RPH', 'MI-UNK', 'MN-APN', 'MN-CNA', 'MN-CNM',
                      'MN-CNS', 'MN-DCH', 'MN-DEN', 'MN-DOS', 'MN-DPM', 'MN-DVM', 'MN-MDR', 'MN-MWF',
                      'MN-NPR', 'MN-ODR', 'MN-PAS', 'MN-RPH', 'MN-UNK', 'MO-APN', 'MO-CNA', 'MO-CNM',
                      'MO-CNS', 'MO-DCH', 'MO-DEN', 'MO-DOS', 'MO-DPM', 'MO-DVM', 'MO-MDR', 'MO-MWF',
                      'MO-NPR', 'MO-ODR', 'MO-PAS', 'MO-RPH', 'MO-UNK', 'MP-UNK', 'MS-APN', 'MS-CNA',
                      'MS-CNM', 'MS-CNS', 'MS-DCH', 'MS-DEN', 'MS-DOS', 'MS-DPM', 'MS-DVM', 'MS-MDR',
                      'MS-MWF', 'MS-NPR', 'MS-ODR', 'MS-PAS', 'MS-RPH', 'MS-UNK', 'MT-APN', 'MT-CNA',
                      'MT-CNM', 'MT-CNS', 'MT-DCH', 'MT-DEN', 'MT-DOS', 'MT-DPM', 'MT-DVM', 'MT-MDR',
                      'MT-MWF', 'MT-NPR', 'MT-ODR', 'MT-PAS', 'MT-RPH', 'MT-UNK', 'NC-APN', 'NC-CNA',
                      'NC-CNM', 'NC-CNS', 'NC-DCH', 'NC-DEN', 'NC-DOS', 'NC-DPM', 'NC-DVM', 'NC-MDR',
                      'NC-MWF', 'NC-NPR', 'NC-ODR', 'NC-PAS', 'NC-RPH', 'NC-UNK', 'ND-APN', 'ND-CNA',
                      'ND-CNM', 'ND-CNS', 'ND-DCH', 'ND-DEN', 'ND-DOS', 'ND-DPM', 'ND-DVM', 'ND-MDR',
                      'ND-MWF', 'ND-NPR', 'ND-ODR', 'ND-PAS', 'ND-RPH', 'ND-UNK', 'NE-APN', 'NE-CNA',
                      'NE-CNM', 'NE-CNS', 'NE-DCH', 'NE-DEN', 'NE-DOS', 'NE-DPM', 'NE-DVM', 'NE-MDR',
                      'NE-MWF', 'NE-NPR', 'NE-ODR', 'NE-PAS', 'NE-RPH', 'NE-UNK', 'NH-APN', 'NH-CNA',
                      'NH-CNM', 'NH-CNS', 'NH-DCH', 'NH-DEN', 'NH-DOS', 'NH-DPM', 'NH-DVM', 'NH-MDR',
                      'NH-MWF', 'NH-NPR', 'NH-ODR', 'NH-PAS', 'NH-RPH', 'NH-UNK', 'NJ-APN', 'NJ-CNA',
                      'NJ-CNM', 'NJ-CNS', 'NJ-DCH', 'NJ-DEN', 'NJ-DOS', 'NJ-DPM', 'NJ-DVM', 'NJ-MDR',
                      'NJ-MWF', 'NJ-NPR', 'NJ-ODR', 'NJ-PAS', 'NJ-RPH', 'NJ-UNK', 'NM-APN', 'NM-CNA',
                      'NM-CNM', 'NM-CNS', 'NM-DCH', 'NM-DEN', 'NM-DOS', 'NM-DPM', 'NM-DVM', 'NM-MDR',
                      'NM-MWF', 'NM-NPR', 'NM-ODR', 'NM-PAS', 'NM-RPH', 'NM-UNK', 'NV-APN', 'NV-CNA',
                      'NV-CNM', 'NV-CNS', 'NV-DCH', 'NV-DEN', 'NV-DOS', 'NV-DPM', 'NV-DVM', 'NV-MDR',
                      'NV-MWF', 'NV-NPR', 'NV-ODR', 'NV-PAS', 'NV-RPH', 'NV-UNK', 'NY-APN', 'NY-CNA',
                      'NY-CNM', 'NY-CNS', 'NY-DCH', 'NY-DEN', 'NY-DPM', 'NY-DVM', 'NY-MDU', 'NY-MWF',
                      'NY-NPR', 'NY-ODR', 'NY-PAS', 'NY-RPH', 'NY-UNK', 'OH-APN', 'OH-CNA', 'OH-CNM',
                      'OH-CNS', 'OH-DCH', 'OH-DEN', 'OH-DOS', 'OH-DPM', 'OH-DVM', 'OH-MDR', 'OH-MWF',
                      'OH-NPR', 'OH-ODR', 'OH-PAS', 'OH-RPH', 'OH-UNK', 'OK-APN', 'OK-CNA', 'OK-CNM',
                      'OK-CNS', 'OK-DCH', 'OK-DEN', 'OK-DOS', 'OK-DPM', 'OK-DVM', 'OK-MDR', 'OK-MWF',
                      'OK-NPR', 'OK-ODR', 'OK-PAS', 'OK-RPH', 'OK-UNK', 'OR-APN', 'OR-CNA', 'OR-CNM',
                      'OR-CNS', 'OR-DCH', 'OR-DEN', 'OR-DOS', 'OR-DPM', 'OR-DVM', 'OR-MDR', 'OR-MWF',
                      'OR-NPR', 'OR-ODR', 'OR-PAS', 'OR-RPH', 'OR-UNK', 'PA-APN', 'PA-CNA', 'PA-CNM',
                      'PA-CNS', 'PA-DCH', 'PA-DEN', 'PA-DOS', 'PA-DPM', 'PA-DVM', 'PA-MDR', 'PA-MWF',
                      'PA-NPR', 'PA-ODR', 'PA-PAS', 'PA-RPH', 'PA-UNK', 'PR-APN', 'PR-CNA', 'PR-CNM',
                      'PR-CNS', 'PR-DCH', 'PR-DEN', 'PR-DPM', 'PR-DVM', 'PR-MDU', 'PR-MWF', 'PR-NPR',
                      'PR-ODR', 'PR-PAS', 'PR-RPH', 'PR-UNK', 'PW-UNK', 'RI-APN', 'RI-CNA', 'RI-CNM',
                      'RI-CNS', 'RI-DCH', 'RI-DEN', 'RI-DOS', 'RI-DPM', 'RI-DVM', 'RI-MDR', 'RI-MWF',
                      'RI-NPR', 'RI-ODR', 'RI-PAS', 'RI-RPH', 'RI-UNK', 'SC-APN', 'SC-CNA', 'SC-CNM',
                      'SC-CNS', 'SC-DCH', 'SC-DEN', 'SC-DOS', 'SC-DPM', 'SC-DVM', 'SC-MDR', 'SC-MWF',
                      'SC-NPR', 'SC-ODR', 'SC-PAS', 'SC-RPH', 'SC-UNK', 'SD-APN', 'SD-CNA', 'SD-CNM',
                      'SD-CNS', 'SD-DCH', 'SD-DEN', 'SD-DOS', 'SD-DPM', 'SD-DVM', 'SD-MDR', 'SD-MWF',
                      'SD-NPR', 'SD-ODR', 'SD-PAS', 'SD-RPH', 'SD-UNK', 'TN-APN', 'TN-CNA', 'TN-CNM',
                      'TN-CNS', 'TN-DCH', 'TN-DEN', 'TN-DOS', 'TN-DPM', 'TN-DVM', 'TN-MDR', 'TN-MWF',
                      'TN-NPR', 'TN-ODR', 'TN-PAS', 'TN-RPH', 'TN-UNK', 'TX-APN', 'TX-CNA', 'TX-CNM',
                      'TX-CNS', 'TX-DCH', 'TX-DEN', 'TX-DOS', 'TX-DPM', 'TX-DVM', 'TX-MDR', 'TX-MWF',
                      'TX-NPR', 'TX-ODR', 'TX-PAS', 'TX-RPH', 'TX-UNK', 'UT-APN', 'UT-CNA', 'UT-CNM',
                      'UT-CNS', 'UT-DCH', 'UT-DEN', 'UT-DOS', 'UT-DPM', 'UT-DVM', 'UT-MDR', 'UT-MWF',
                      'UT-NPR', 'UT-ODR', 'UT-PAS', 'UT-RPH', 'UT-UNK', 'VA-APN', 'VA-CNA', 'VA-CNM',
                      'VA-CNS', 'VA-DCH', 'VA-DEN', 'VA-DOS', 'VA-DPM', 'VA-DVM', 'VA-MDR', 'VA-MWF',
                      'VA-NPR', 'VA-ODR', 'VA-PAS', 'VA-RPH', 'VA-UNK', 'VI-APN', 'VI-CNA', 'VI-CNM',
                      'VI-CNS', 'VI-DCH', 'VI-DEN', 'VI-DOS', 'VI-DPM', 'VI-DVM', 'VI-MDR', 'VI-MWF',
                      'VI-NPR', 'VI-ODR', 'VI-PAS', 'VI-RPH', 'VI-UNK', 'VT-APN', 'VT-CNA', 'VT-CNM',
                      'VT-CNS', 'VT-DCH', 'VT-DEN', 'VT-DOS', 'VT-DPM', 'VT-DVM', 'VT-MDR', 'VT-MWF',
                      'VT-NPR', 'VT-ODR', 'VT-PAS', 'VT-RPH', 'VT-UNK', 'WA-APN', 'WA-CNA', 'WA-CNM',
                      'WA-CNS', 'WA-DCH', 'WA-DEN', 'WA-DOS', 'WA-DPM', 'WA-DVM', 'WA-MDR', 'WA-MWF',
                      'WA-NPR', 'WA-ODR', 'WA-PAS', 'WA-RPH', 'WA-UNK', 'WI-APN', 'WI-CNA', 'WI-CNM',
                      'WI-CNS', 'WI-DCH', 'WI-DEN', 'WI-DOS', 'WI-DPM', 'WI-DVM', 'WI-MDR', 'WI-MWF',
                      'WI-NPR', 'WI-ODR', 'WI-PAS', 'WI-RPH', 'WI-UNK', 'WV-APN', 'WV-CNA', 'WV-CNM',
                      'WV-CNS', 'WV-DCH', 'WV-DEN', 'WV-DOS', 'WV-DPM', 'WV-DVM', 'WV-MDR', 'WV-MWF',
                      'WV-NPR', 'WV-ODR', 'WV-PAS', 'WV-RPH', 'WV-UNK', 'WY-APN', 'WY-CNA', 'WY-CNM',
                      'WY-CNS', 'WY-DCH', 'WY-DEN')

ADDRESS_PURPOSE = (
    "LOCATION",
    "MAILING",
    "MEDREC-STORAGE",
    "1099",
    "REVALIDATION",
    "ADDITIONAL-LOCATION",
    "REMITTANCE",
    "TELEMEDICINE",
    "ADDITIONAL-DOCUMENTATION-REQUESTS")

ADDRESS_TYPE = ('DOM', 'MIL', 'FGN')

STATES = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
          'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
          'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
          'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
          'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
          'WY', 'AS', 'FM', 'GU', 'MH', 'MP', 'PR', 'PW', 'VI', 'ZZ')

COUNTRIES = ('AF', 'AX', 'AL', 'DZ', 'AS',
             'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT',
             'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM',
             'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG',
             'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL',
             'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI',
             'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC',
             'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI',
             'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI',
             'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY',
             'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR',
             'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ',
             'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS',
             'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY',
             'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM',
             'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR',
             'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP',
             'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH',
             'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL',
             'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA',
             'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO',
             'ZA', 'GS', 'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE',
             'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO',
             'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB',
             'US', 'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF',
             'EH', 'YE', 'ZM', 'ZW')
