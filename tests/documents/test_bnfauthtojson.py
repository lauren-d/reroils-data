# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""BNFAUTHTOJSON module tests."""

from __future__ import absolute_import, print_function

from dojson.contrib.marc21.utils import create_record

from reroils_data.documents.dojson.contrib.bnfauthtojson import bnfauthtojson


# identifier_for_person: [003]
def test_bnf_auth_to_identifier_for_person():
    """Test dojson bnf_auth_to_identifier_for_person."""

    http = 'http://data.bnf.fr/ark:/12148/cb10356443j'
    marcxml = """
    <record>
      <controlfield tag="003">{}</controlfield>
    </record>
    """.format(http)
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    identifier_for_person = data.get('identifier_for_person')
    assert identifier_for_person.get('source') == 'bnf'
    assert identifier_for_person.get('value') == http


# # date_of_birth: [103|200]
# def test_bnf_auth_to_date_of_birth():
#     """Test dojson bnf_auth_to_date_of_birth."""
#
#     marcxml = """
#     <record>
#       <datafield tag="103" ind1=" " ind2=" ">
#         <subfield code="a"> 18030724  18840211 </subfield>
#       </datafield>
#     </record>
#     """
#     marcjson = create_record(marcxml)
#     data = bnfauthtojson.do(marcjson)
#     assert data.get('date_of_birth') == {
#         'source': 'bnf',
#         'value': '1803-07-24'
#     }
#
#     marcxml = """
#     <record>
#       <datafield tag="103" ind1=" " ind2=" ">
#         <subfield code="a"> 17820222  1860    ?</subfield>
#       </datafield>
#       <datafield tag="200" ind1=" " ind2="|">
#         <subfield code="7">ba0yba0y</subfield>
#         <subfield code="8">fre   </subfield>
#         <subfield code="9"> 0 </subfield>
#         <subfield code="a">Arnoult</subfield>
#         <subfield code="b">Stéphen</subfield>
#         <subfield code="f">1782-1860?</subfield>
#       </datafield>
#     </record>
#     """
#     marcjson = create_record(marcxml)
#     data = bnfauthtojson.do(marcjson)
#     assert data.get('date_of_birth') == {
#         'source': 'bnf',
#         'value': '1782-02-22'
#     }
#
#     marcxml = """
#     <record>
#       <datafield tag="200" ind1=" " ind2="|">
#         <subfield code="7">ba0yba0y</subfield>
#         <subfield code="8">fre   </subfield>
#         <subfield code="9"> 0 </subfield>
#         <subfield code="a">Arnoult</subfield>
#         <subfield code="b">Stéphen</subfield>
#         <subfield code="f">1782-1860?</subfield>
#       </datafield>
#     </record>
#     """
#     marcjson = create_record(marcxml)
#     data = bnfauthtojson.do(marcjson)
#     assert data.get('date_of_birth') == {
#         'source': 'bnf',
#         'value': '1782'
#     }


# gender: [120$a]
def test_bnf_auth_to_gender():
    """Test dojson bnf_auth_to_gender."""

    marcxml = """
    <record>
      <datafield tag="120" ind1="1" ind2="0">
        <subfield code="a">a</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('gender') == 'female'


# language_of_person: [101$a repetitive]
def test_bnf_auth_to_language_of_person():
    """Test dojson bnf_auth_to_language_of_person."""

    marcxml = """
    <record>
      <datafield tag="101" ind1="1" ind2="0">
        <subfield code="a">eng</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('language_of_person') == ('eng',)

    marcxml = """
    <record>
      <datafield tag="101" ind1="1" ind2="0">
        <subfield code="a">eng</subfield>
        <subfield code="a">ger</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('language_of_person') == ('eng', 'ger')


# biographical_information: [300$a 34x$a repetitive]
def test_bnf_auth_to_biographical_information():
    """Test dojson bnf_auth_to_biographical_information."""

    marcxml = """
    <record>
      <datafield tag="300" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    biographical_informations = data.get('biographical_information')
    assert biographical_informations == [
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux'
        }
    ]

    marcxml = """
    <record>
      <datafield tag="300" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux</subfield>
      </datafield>
      <datafield tag="341" ind1="1" ind2="0">
        <subfield code="a">Chef des bureaux 2</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    biographical_informations = data.get('biographical_information')
    assert biographical_informations == [
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux'
        },
        {
            'source': 'bnf',
            'language': 'fre',
            'value': 'Chef des bureaux 2'
        }
    ]


# preferred_name_for_person: [200$ab]
def test_bnf_auth_to_preferred_name_for_person():
    """Test dojson bnf_auth_to_preferred_name_for_person."""

    marcxml = """
    <record>
      <datafield tag="200" ind1=" " ind2="|">
        <subfield code="7">ba0yba0y</subfield>
        <subfield code="8">fre   </subfield>
        <subfield code="9"> 0 </subfield>
        <subfield code="a">Aldo</subfield>
        <subfield code="b">Dr</subfield>
        <subfield code="f">1813-1875</subfield>
      </datafield>
    </record>
    """
    marcjson = create_record(marcxml)
    data = bnfauthtojson.do(marcjson)
    assert data.get('preferred_name_for_person') == {
        'source': 'bnf',
        'language': 'fre',
        'value': 'Aldo, Dr'
    }
