#
# Copyright (c) 2015, Prometheus Research, LLC
#


import json
import os

import pytest

from rios.core.validation.instrument import Instrument, ValidationError, \
    get_full_type_definition, TYPES_ALL

from utils import *


GOOD_INSTRUMENT_FILES = os.path.join(EXAMPLE_FILES, 'instruments/good')
@pytest.mark.parametrize('filename', get_example_files(GOOD_INSTRUMENT_FILES))
def test_good_files(filename):
    check_good_validation(Instrument(), os.path.join(
        GOOD_INSTRUMENT_FILES,
        filename,
    ))


BAD_INSTRUMENT_FILES = os.path.join(EXAMPLE_FILES, 'instruments/bad')
@pytest.mark.parametrize('filename', get_example_files(BAD_INSTRUMENT_FILES))
def test_bad_files(filename):
    check_bad_validation(Instrument(), os.path.join(
        BAD_INSTRUMENT_FILES,
        filename,
    ))



GFTD_TESTER = {
    'id': 'urn:type-tester',
    'version': '1.0',
    'title': 'A Instrument to Test Types and Inheritance',
    'types': {
        'customText': {
            'base': 'text',
            'pattern': 'foo',
        },
        'customText2': {
            'base': 'customText',
            'length': {
                'min': 2
            },
        },
    },
    'record': [
        {
            'id': 'field1',
            'type': 'text'
        }
    ],
}


@pytest.mark.parametrize('type_id', TYPES_ALL)
def test_gftd_base_id(type_id):
    type_def = get_full_type_definition(GFTD_TESTER, type_id)
    assert isinstance(type_def, dict)
    assert len(list(type_def.keys())) == 1
    assert type_def['base'] == type_id

def test_gftd_custom_id():
    type_def = get_full_type_definition(GFTD_TESTER, 'customText')
    assert isinstance(type_def, dict)
    assert len(list(type_def.keys())) == 2
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'foo'


def test_gftd_inherited_custom_id():
    type_def = get_full_type_definition(GFTD_TESTER, 'customText2')
    assert isinstance(type_def, dict)
    assert len(list(type_def.keys())) == 3
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'foo'
    assert isinstance(type_def['length'], dict)
    assert len(list(type_def['length'].keys())) == 1
    assert type_def['length']['min'] == 2


def test_gtfd_custom_def():
    custom_def = {
        'base': 'text',
        'pattern': 'bar',
    }
    type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    assert isinstance(type_def, dict)
    assert len(list(type_def.keys())) == 2
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'bar'


def test_gtfd_inherited_custom_def():
    custom_def = {
        'base': 'customText2',
        'pattern': 'bar',
    }
    type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    assert isinstance(type_def, dict)
    assert len(list(type_def.keys())) == 3
    assert type_def['base'] == 'text'
    assert type_def['pattern'] == 'bar'
    assert isinstance(type_def['length'], dict)
    assert len(list(type_def['length'].keys())) == 1
    assert type_def['length']['min'] == 2


def test_gftd_unknown_id():
    try:
        type_def = get_full_type_definition(GFTD_TESTER, 'foobar')
    except ValueError as exc:
        assert 'no type is defined for identifier' in str(exc)
    else:
        assert False, 'gftd did not fail, got %r' % type_def


def test_gtfd_unknown_def_base():
    custom_def = {
        'base': 'foobar',
        'pattern': 'bar',
    }
    try:
        type_def = get_full_type_definition(GFTD_TESTER, custom_def)
    except ValueError as exc:
        assert 'references undefined base' in str(exc)
    else:
        assert False, 'gftd did not fail, got %r' % type_def


def test_gftd_bad_input():
    try:
        type_def = get_full_type_definition(GFTD_TESTER, False)
    except TypeError as exc:
        assert 'type_def must be a string or dict' in str(exc)
    else:
        assert False, 'gftd did not fail, got %r' % type_def

