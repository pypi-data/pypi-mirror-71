#
# Copyright (c) 2015, Prometheus Research, LLC
#


import re

from copy import deepcopy
from datetime import datetime

import colander

from six import iteritems, string_types, integer_types

from .common import ValidationError, sub_schema, AnyType, LanguageTag, \
    validate_instrument_version, MetadataCollection, RE_PRODUCT_TOKENS
from .instrument import InstrumentReference, IdentifierString, \
    get_full_type_definition


__all__ = (
    'METADATA_PROPS_ASSESSMENT',
    'METADATA_PROPS_VALUE',

    'ValueCollection',
    'Assessment',
)


RE_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
RE_TIME = re.compile(r'^\d{2}:\d{2}:\d{2}$')
RE_DATETIME = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$')

METADATA_PROPS_ASSESSMENT = {
    'language': LanguageTag(),
    'application': colander.SchemaNode(
        colander.String(),
        validator=colander.Regex(RE_PRODUCT_TOKENS),
    ),
    'dateCompleted': colander.SchemaNode(
        colander.DateTime(),
    ),
    'timeTaken': colander.SchemaNode(
        colander.Integer(),
    ),
}

METADATA_PROPS_VALUE = {
    'timeTaken': colander.SchemaNode(
        colander.Integer(),
    ),
}


# pylint: disable=abstract-method


class Value(colander.SchemaNode):
    value = colander.SchemaNode(
        AnyType(),
    )
    explanation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    annotation = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )
    meta = MetadataCollection(
        METADATA_PROPS_VALUE,
        missing=colander.drop,
    )

    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Value, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if isinstance(cstruct['value'], list):
            for subtype in (
                    colander.SchemaNode(colander.String()),
                    ValueCollection):
                for value in cstruct['value']:
                    try:
                        sub_schema(subtype, node, value)
                    except ValidationError:
                        break
                else:
                    return

            raise ValidationError(
                node,
                'Lists must be consist only of Strings or ValueCollections',
            )

        if isinstance(cstruct['value'], dict):
            sub_schema(ValueCollectionMapping, node, cstruct['value'])


class ValueCollection(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollection, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if not cstruct:
            raise ValidationError(
                node,
                'At least one Value must be defined',
            )

        for field_id, value in iteritems(cstruct):
            sub_schema(IdentifierString, node, field_id)
            sub_schema(Value, node, value)


class ValueCollectionMapping(colander.SchemaNode):
    def __init__(self, *args, **kwargs):
        kwargs['typ'] = colander.Mapping(unknown='preserve')
        super(ValueCollectionMapping, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        cstruct = cstruct or {}
        if not cstruct:
            raise ValidationError(
                node,
                'At least one Row must be defined',
            )

        for field_id, values in iteritems(cstruct):
            sub_schema(IdentifierString, node, field_id)
            sub_schema(ValueCollection, node, values)


VALUE_TYPE_CHECKS = {
    'integer': lambda val: isinstance(val, integer_types),
    'float': lambda val: isinstance(val, (float,) + integer_types),
    'text': lambda val: isinstance(val, string_types),
    'enumeration': lambda val: isinstance(val, string_types),
    'boolean': lambda val: isinstance(val, bool),
    'date': lambda val: isinstance(val, string_types) and RE_DATE.match(val),
    'time': lambda val: isinstance(val, string_types) and RE_TIME.match(val),
    'dateTime':
    lambda val: isinstance(val, string_types) and RE_DATETIME.match(val),
    'enumerationSet': lambda val: isinstance(val, list),
    'recordList': lambda val: isinstance(val, list),
    'matrix': lambda val: isinstance(val, dict),
}


class Assessment(colander.SchemaNode):
    instrument = InstrumentReference()
    meta = MetadataCollection(
        METADATA_PROPS_ASSESSMENT,
        missing=colander.drop,
    )
    values = ValueCollection()

    def __init__(self, *args, **kwargs):
        self.instrument = kwargs.pop('instrument', None)
        kwargs['typ'] = colander.Mapping(unknown='raise')
        super(Assessment, self).__init__(*args, **kwargs)

    def validator(self, node, cstruct):
        if not self.instrument:
            return

        validate_instrument_version(
            self.instrument,
            cstruct,
            node.get('instrument'),
        )

        self.check_has_all_fields(
            node.get('values'),
            cstruct['values'],
            self.instrument['record'],
        )

    def check_has_all_fields(self, node, values, fields):
        values = deepcopy(values)
        if not isinstance(values, dict):
            raise ValidationError(
                node,
                'Value expected to contain a mapping: %s' % values
            )

        for field in fields:
            value = values.pop(field['id'], None)
            fid = field['id']
            if value is None:
                raise ValidationError(
                    node,
                    'No value exists for field ID "%s"' % fid,
                )

            if value['value'] is None and field.get('required', False):
                raise ValidationError(
                    node,
                    'No value present for required field ID "%s"' % fid,
                )

            full_type_def = get_full_type_definition(
                self.instrument,
                field['type'],
            )

            self._check_value_type(node, value['value'], field, full_type_def)

            self._check_value_constraints(
                node,
                value['value'],
                field,
                full_type_def,
            )

            self._check_metafields(node, value, field)

            self._check_complex_subfields(node, full_type_def, value)

        if values:
            raise ValidationError(
                node,
                'Unknown field IDs found: %s' % ', '.join(list(values.keys())),
            )

    def _check_value_type(self, node, value, field, type_def):
        if value is None:
            return

        wrong_type_error = ValidationError(
            node,
            'Value for "%s" is not of the correct type' % (
                field['id'],
            ),
        )

        bad_choice_error = ValidationError(
            node,
            'Value for "%s" is not an accepted enumeration' % (
                field['id'],
            ),
        )

        # Basic checks
        if not VALUE_TYPE_CHECKS[type_def['base']](value):
            raise wrong_type_error

        # Deeper checks
        if type_def['base'] == 'enumerationSet':
            choices = list(type_def['enumerations'].keys())
            for subval in value:
                if not isinstance(subval, string_types):
                    raise wrong_type_error
                if subval not in choices:
                    raise bad_choice_error
        elif type_def['base'] == 'enumeration':
            choices = list(type_def['enumerations'].keys())
            if value not in choices:
                raise bad_choice_error

    def _check_value_constraints(self, node, value, field, type_def):
        if value is None:
            return

        if type_def.get('pattern'):
            regex = re.compile(type_def['pattern'])
            if not regex.match(value):
                raise ValidationError(
                    node,
                    'Value for "%s" does not match the specified pattern' % (
                        field['id'],
                    ),
                )

        if type_def.get('length'):
            if type_def['length'].get('min') is not None \
                    and len(value) < type_def['length']['min']:
                raise ValidationError(
                    node,
                    'Value for "%s" is less than acceptible minimum'
                    ' length' % (
                        field['id'],
                    ),
                )
            if type_def['length'].get('max') is not None \
                    and len(value) > type_def['length']['max']:
                raise ValidationError(
                    node,
                    'Value for "%s" is greater than acceptible maximum'
                    ' length' % (
                        field['id'],
                    ),
                )

        if type_def.get('range'):
            casted_value = self._cast_range(value, type_def['base'])

            casted_min = self._cast_range(
                type_def['range']['min'],
                type_def['base'],
            )
            if type_def['range'].get('min') is not None \
                    and casted_value < casted_min:
                raise ValidationError(
                    node,
                    'Value for "%s" is less than acceptible minimum' % (
                        field['id'],
                    ),
                )

            casted_max = self._cast_range(
                type_def['range']['max'],
                type_def['base'],
            )
            if type_def['range'].get('max') is not None \
                    and casted_value > casted_max:
                raise ValidationError(
                    node,
                    'Value for "%s" is greater than acceptible maximum' % (
                        field['id'],
                    ),
                )

    def _cast_range(self, value, type_base):
        if type_base in ('integer', 'float'):
            return value
        if type_base == 'date':
            return datetime.strptime(value, '%Y-%m-%d').date()
        if type_base == 'dateTime':
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        if type_base == 'time':
            return datetime.strptime(value, '%H:%M:%S').time()
        return None

    def _check_metafields(self, node, value, field):
        explanation = field.get('explanation', 'none')
        fid = field['id']
        if 'explanation' in value \
                and value['explanation'] is not None \
                and explanation == 'none':
            raise ValidationError(
                node,
                'Explanation present where not allowed in field ID "%s"' % fid,
            )
        if 'explanation' not in value and explanation == 'required':
            raise ValidationError(
                node,
                'Explanation missing for field ID "%s"' % fid,
            )

        annotation = field.get('annotation', 'none')
        if 'annotation' in value and value['annotation'] is not None:
            if annotation == 'none':
                raise ValidationError(
                    node,
                    'Annotation present where not allowed: %s' % fid,
                )

            if value['value'] is not None:
                raise ValidationError(
                    node,
                    'Annotation provided for non-empty value: %s' % fid,
                )
        elif 'annotation' not in value \
                and annotation == 'required' \
                and value['value'] is None:
            raise ValidationError(
                node,
                'Annotation missing for field ID "%s"' % fid,
            )

    def _check_complex_subfields(self, node, full_type_def, value):
        if value['value'] is None:
            return

        if 'record' in full_type_def:
            for rec in value['value']:
                self.check_has_all_fields(
                    node,
                    rec,
                    full_type_def['record'],
                )

        elif 'rows' in full_type_def:
            self._check_matrix_subfields(node, full_type_def, value)

    def _check_matrix_subfields(self, node, full_type_def, value):
        for row in full_type_def['rows']:
            row_value = value['value'].pop(row['id'], None)
            if row_value is None:
                raise ValidationError(
                    node,
                    'Missing values for row ID "%s"' % row['id'],
                )

            # Make sure all the columns exist.
            columns = set([
                column['id']
                for column in full_type_def['columns']
            ])
            existing_columns = set(row_value.keys())
            missing_columns = columns - existing_columns
            if missing_columns:
                raise ValidationError(
                    node,
                    'Row ID "%s" is missing values for columns: %s' % (
                        row['id'],
                        ', '.join(list(missing_columns)),
                    ),
                )
            extra_columns = existing_columns - columns
            if extra_columns:
                raise ValidationError(
                    node,
                    'Row ID "%s" contains unknown column IDs: %s' % (
                        row['id'],
                        ', '.join(list(extra_columns)),
                    ),
                )

            # Enforce row requirements.
            columns_with_values = [
                column
                for column in existing_columns
                if row_value[column]['value'] is not None
            ]
            if row.get('required', False) and not columns_with_values:
                raise ValidationError(
                    node,
                    'Row ID "%s" requires at least one column with a'
                    ' value' % (
                        row['id'],
                    ),
                )

            # Enforce column requirements.
            required_columns = [
                column['id']
                for column in full_type_def['columns']
                if column.get('required', False)
            ]
            if required_columns and columns_with_values:
                missing = set(required_columns) - set(columns_with_values)
                if missing:
                    raise ValidationError(
                        node,
                        'Row ID "%s" is missing values for columns: %s' % (
                            row['id'],
                            ', '.join(list(missing)),
                        ),
                    )

            for column in full_type_def['columns']:
                type_def = get_full_type_definition(
                    self.instrument,
                    column['type'],
                )

                self._check_value_type(
                    node,
                    row_value[column['id']]['value'],
                    column,
                    type_def,
                )
                self._check_value_constraints(
                    node,
                    row_value[column['id']]['value'],
                    column,
                    type_def,
                )

        if value['value']:
            raise ValidationError(
                node,
                'Unknown row IDs found: %s' % (
                    ', '.join(list(value['value'].keys())),
                ),
            )

