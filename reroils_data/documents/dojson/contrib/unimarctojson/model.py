# -*- coding: utf-8 -*-
#
# This file is part of BiblioMedia-Data
# Copyright (C) 2016 RERO.
#
# BiblioMedia-Data is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Bibliomedia UNIMARC model definition."""

import re
from json import loads

from dojson import Overdo, utils
# from dojson.utils import force_list
from pkg_resources import resource_string

unimarctojson = Overdo()


# @unimarctojson.over('__order__', '__order__')
# def order(self, key, value):
#     """Preserve order of datafields."""
#     order = []
#     for field in value:
#         name = unimarctojson.index.query(field)
#         if name:
#             name = name[0]
#         else:
#             name = field
#         order.append(name)
#
#     return order


@unimarctojson.over('identifiers', '^003')
@utils.ignore_value
def unimarcbnfid(self, key, value):
    """Get ID.

    identifier bnfID 003
    """
    values = value.split('/')
    identifiers = self.get('identifiers', {})
    identifiers['bnfID'] = values[-1]
    return identifiers


@unimarctojson.over('title', '^200..')
@utils.ignore_value
def unimarctitle(self, key, value):
    """Get title.

    title: 200$a
    If there's a $e, then 245$a : $e
    """
    main_title = value.get('a')
    sub_title = value.get('e')
    # responsability = value.get('c')
    if sub_title:
        main_title += ' : ' + ' : '.join(
            utils.force_list(sub_title)
        )
    return main_title


@unimarctojson.over('titlesProper', '^500..')
@utils.for_each_value
@utils.ignore_value
def unimarctitlesProper(self, key, value):
    """Test dojson unimarctitlesProper.

    titleProper: 500$a
    """
    return value.get('a')


@unimarctojson.over('languages', '^101')
@utils.ignore_value
def unimarclanguages(self, key, value):
    """Get languages.

    languages: 008 and 041 [$a, repetitive]
    """
    languages = utils.force_list(value.get('a'))
    to_return = []
    schema_in_bytes = resource_string('reroils_data.documents.jsonschemas',
                                      'documents/book-v0.0.1.json')
    schema = loads(schema_in_bytes.decode('utf8'))
    langs = schema[
        'properties']['languages']['items']['properties']['language']['enum']
    for language in languages:
        if language in langs:
            to_return.append({'language': language})

    translatedsfrom = utils.force_list(value.get('c'))
    if translatedsfrom:
        self['translatedFrom'] = []
        for translatedfrom in translatedsfrom:
            self['translatedFrom'].append(translatedfrom)

    return to_return


@unimarctojson.over('authors', '7[01][012]..')
@utils.for_each_value
@utils.ignore_value
def unimarctoauthor(self, key, value):
    """Get author.

    authors: loop:
    700 Nom de personne – Responsabilité principale
    701 Nom de personne – Autre responsabilité principale
    702 Nom de personne – Responsabilité secondaire
    710 Nom de collectivité – Responsabilité principale
    711 Nom de collectivité – Autre responsabilité principale
    712 Nom de collectivité – Responsabilité secondaire
    """
    author = {}
    author['name'] = value.get('a')
    author['type'] = 'person'
    if key[1] == '1':
        author['type'] = 'organisation'

    if value.get('b'):
        author['name'] += ', ' + value.get('b')
    if value.get('d'):
        author['name'] += ' ' + value.get('d')

    if value.get('c'):
        author['qualifier'] = value.get('c')

    if value.get('f'):
        date = value.get('f')
        date = date.replace('-....', '-')
        author['date'] = date
    return author


@unimarctojson.over('publishers', '^210..')
@utils.ignore_value
def unimarcpublishers_publicationDate(self, key, value):
    """Get publisher.

    publisher.name: 210 [$b repetitive]
    publisher.place: 210 [$a repetitive]
    publicationDate: 210 [$c repetitive] (take only the first one)
    """
    lasttag = '?'
    publishers = self.get('publishers', [])

    publisher = {}
    indexes = {}
    lasttag = '?'
    for tag in value['__order__']:
        index = indexes.get(tag, 0)
        data = value[tag]
        if type(data) == tuple:
            data = data[index]
        if tag == 'a' and index > 0 and lasttag != 'a':
            publishers.append(publisher)
            publisher = {}
        if tag == 'a':
            place = publisher.get('place', [])
            place.append(data)
            publisher['place'] = place
        elif tag == 'c':
            name = publisher.get('name', [])
            name.append(data)
            publisher['name'] = name
        elif tag == 'd' and index == 0:

            # 4 digits
            date = re.match(r'.*?(\d{4})', data).group(1)
            self['publicationYear'] = int(date)

            # create free form if different
            if data != str(self['publicationYear']):
                self['freeFormedPublicationDate'] = data
        indexes[tag] = index + 1
        lasttag = tag
    publishers.append(publisher)
    return publishers


@unimarctojson.over('formats', '^215..')
@utils.ignore_value
def unimarcdescription(self, key, value):
    """Get extent, otherMaterialCharacteristics, formats.

    extent: 215$a (the first one if many)
    otherMaterialCharacteristics: 215$b (the first one if many)
    formats: 215 [$c repetitive]
    """
    if value.get('a'):
        if not self.get('extent', None):
            self['extent'] = (
                utils.force_list(value.get('a'))[0]
            )
    if value.get('c'):
        if self.get('otherMaterialCharacteristics', []) == []:
            self['otherMaterialCharacteristics'] = (
                utils.force_list(value.get('c'))[0]
            )
    if value.get('d'):
        formats = self.get('formats', None)
        if not formats:
            data = value.get('d')
            formats = list(utils.force_list(data))
        return formats
    else:
        return None


@unimarctojson.over('series', '^225..')
@utils.for_each_value
@utils.ignore_value
def unimarcseries(self, key, value):
    """Get series.

    series.name: [225$a repetitive]
    series.number: [225$v repetitive]
    """
    series = {}
    name = value.get('a')
    if name:
        series['name'] = ', '.join(utils.force_list(name))
    number = value.get('v')
    if number:
        series['number'] = ', '.join(utils.force_list(number))
    return series


@unimarctojson.over('abstracts', '^330..')
@utils.for_each_value
@utils.ignore_value
def unimarcabstracts(self, key, value):
    """Get abstracts.

    abstract: [330$a repetitive]
    """
    return ', '.join(utils.force_list(value.get('a')))


@unimarctojson.over('identifiers', '^073..')
@utils.ignore_value
def unimarcidentifier_isbn(self, key, value):
    """Get identifier isbn.

    identifiers:isbn: 010$a
    """
    identifiers = self.get('identifiers', {})
    if value.get('a'):
        identifiers['isbn'] = value.get('a')
    return identifiers


@unimarctojson.over('notes', '^300..')
@utils.for_each_value
@utils.ignore_value
def unimarcnotes(self, key, value):
    """Get  notes.

    note: [300$a repetitive]
    """
    return value.get('a')


@unimarctojson.over('subjects', '^6((0[0-9])|(1[0-7]))..')
@utils.for_each_value
@utils.ignore_value
def unimarcsubjects(self, key, value):
    """Get subjects.

    subjects: 6xx [duplicates could exist between several vocabularies,
        if possible deduplicate]
    """
    to_return = ''
    if value.get('a'):
        to_return = value.get('a')
    if value.get('b'):
        to_return += ', ' + value.get('b')
    if value.get('d'):
        to_return += ' ' + value.get('d')
    if value.get('c'):
        to_return += ', ' + value.get('c')
    if value.get('f'):
        to_return += ', ' + value.get('f')
    return to_return
