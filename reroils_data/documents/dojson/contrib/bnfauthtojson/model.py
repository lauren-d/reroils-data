# -*- coding: utf-8 -*-
#
# This file is part of BiblioMedia-Data
# Copyright (C) 2016 RERO.
#
# BiblioMedia-Data is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

""" BNF auth model definition."""

from dojson import Overdo, utils
from dojson.utils import force_list

bnfauthtojson = Overdo()


@bnfauthtojson.over('identifier_for_person', '^003')
@utils.ignore_value
def bnf_auth_to_identifier_for_person(self, key, value):
    """Get identifier for person.

    identifier_for_person: 003
    """
    to_return = {
        'source': 'bnf',
        'value': value
    }
    return to_return

# @bnfauthtojson.over('date_of_birth', '^(103|200)..')
# @utils.ignore_value
# def bnf_auth_to_date_of_birth(self, key, value):
#     """Get Date of Birth.
#
#     date_of_birth: 103|200
#     """
#     date_of_birth = None
#     if key[:3] == "200" and self.get('date_of_birth') is None:
#         try:
#             date_of_birth = value.get('f').split('-')[0]
#         except:
#             pass
#     elif key[:3] == "103":
#         try:
#             first_date = value.get('a')[1:].split(' ')[0]
#             date_of_birth = first_date[0:4]
#             try:
#                 date_of_birth += '-' + first_date[4:6]
#             except:
#                 pass
#             try:
#                 date_of_birth += '-' + first_date[6:8]
#             except:
#                 pass
#         except:
#             pass
#
#     if date_of_birth:
#         return {
#             'source': 'bnf',
#             'value': date_of_birth
#         }
#     return None

@bnfauthtojson.over('gender', '^120..')
@utils.ignore_value
def bnf_auth_to_gender(self, key, value):
    """Get gender of person.

    gender: 120$a
    """
    gender = value.get('a')
    to_return = 'not known'
    if gender == 'a':
        to_return = 'female'
    elif gender == 'b':
        to_return = 'male'
    return to_return


@bnfauthtojson.over('language_of_person', '^101..')
@utils.ignore_value
def bnf_auth_to_language_of_person(self, key, value):
    """Get language of person.

    language_of_person: 101$a
    """
    return force_list(value.get('a'))

@bnfauthtojson.over('biographical_information', '^(300)|(34.)..')
@utils.for_each_value
@utils.ignore_value
def bnf_auth_to_biographical_information(self, key, value):
    """Get biographical information.

    biographical_information: 300$a
    """
    biographical_information = {
        'source': 'bnf',
        'language': 'fre',
        'value': value.get('a')
    }
    return biographical_information


@bnfauthtojson.over('preferred_name_for_person', '^200..')
@utils.ignore_value
def bnf_auth_to_preferred_name_for_person(self, key, value):
    """Get Preferred Name for Person.

    preferred_name_for_person: 200$ab
    """
    preferred_name_for_person = {
        'source': 'bnf',
        'language': 'fre',
        'value': value.get('a') + ', ' + value.get('b')
    }
    return preferred_name_for_person
