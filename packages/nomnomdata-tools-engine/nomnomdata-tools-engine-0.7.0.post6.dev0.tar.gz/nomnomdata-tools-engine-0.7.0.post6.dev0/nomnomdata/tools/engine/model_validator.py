import logging
from pprint import pformat

from cerberus.validator import Validator

from .code_sql_types import code_types, sql_types

_logger = logging.getLogger(__name__)

parameter_types = [
    "code",
    "json",
    "sql",
    "metadata_table",
    "boolean",
    "connection",
    "text",
    "int",
    "string",
    "enum",
]
help_schema = {
    "oneof_schema": [
        {"header_id": {"type": "string", "required": False}},
        {"file": {"type": "string", "required": False}},
    ],
    "type": "dict",
}


parameter_field_schema = {
    "help": help_schema.copy(),
    "collapsed": {"required": False, "type": "boolean"},
    "required": {"required": False, "type": "boolean"},
    "choices": {"dependencies": {"type": ["enum"]}, "type": "list"},
    "connection_type_uuid": {"dependencies": {"type": ["connection"]}, "type": "string"},
    "name": {"type": "string", "required": True},
    "dialect": {
        "type": "string",
        "oneof": [
            # If type is "sql", only check the list of sql types.
            # If type is "code", only check the list of language types (excluding sql).
            {"dependencies": {"type": ["sql"]}, "allowed": sql_types},
            {"dependencies": {"type": ["code"]}, "allowed": code_types},
        ],
    },
    "description": {"type": "string", "required": False},
    "display_name": {"type": "string", "required": True},
    "type": {
        "allowed": parameter_types,
        "required": True,
        "oneof": [
            # Bi-lateral dependencies
            # E.G. a field that is a "connection" type must have "connection_type_uuid" as a parameter.
            {"allowed": ["connection"], "dependencies": "connection_type_uuid"},
            {"allowed": ["code", "sql"], "dependencies": "dialect"},
            {"allowed": ["enum"], "dependencies": "choices"},
            # Add above bi-lateral dependencies as "forbidden" so above dependencies are evaluated only once.
            {"forbidden": ["connection", "code", "sql", "enum"]},
        ],
    },
    "shared_object_type_uuid": {"type": "string", "required": False},
    "max": {"required": False, "type": "integer"},
    "min": {"required": False, "type": "integer"},
    "default": {"required": False},
}
parameter_group_schema = {
    "display_name": {"type": "string", "required": True},
    "collapsed": {"required": False, "type": "boolean",},
    "shared_parameter_group_uuid": {
        "required": False,
        "dependencies": {"type": ["group"]},
        "type": "string",
    },
    "description": {"type": "string", "required": False},
    "name": {"type": "string", "required": True},
    "type": {"allowed": ["group"], "required": True},
    "parameters": {
        "type": "list",
        "schema": {"type": "dict", "schema": parameter_field_schema.copy()},
    },
}


engine_schema = {
    "uuid": {
        "type": "string",
        "minlength": 8,
        "required": True,
        "regex": r"^[A-Z\d]+-[A-Z\d]+$",
    },
    "icons": {
        "type": "dict",
        "schema": {
            "1x": {"type": "string"},
            "2x": {"type": "string"},
            "3x": {"type": "string"},
        },
    },
    "help": help_schema.copy(),
    "alias": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "nnd_model_version": {"type": "integer", "required": True},
    "options": {"required": False, "type": "dict"},
    "location": {
        "type": "dict",
        "schema": {
            "repo": {"type": "string", "required": True},
            "image": {"type": "string", "required": True},
            "region": {"type": "string", "required": True},
            "repo_type": {"type": "string", "required": True},
        },
    },
    "categories": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {"name": {"type": "string", "required": True}},
        },
    },
    "type": {"allowed": ["engine"], "required": True},
    "actions": {
        "type": "dict",
        "required": True,
        "keyschema": {"type": "string"},
        "valueschema": {
            "type": "dict",
            "schema": {
                "description": {"type": "string", "required": True},
                "help": help_schema.copy(),
                "display_name": {"type": "string", "required": True},
                "parameters": {
                    "type": "list",
                    "required": True,
                    "schema": {"type": "dict", "schema": parameter_group_schema},
                },
            },
        },
    },
}


shared_object_type_schema = {
    "uuid": {
        "type": "string",
        "minlength": 8,
        "required": True,
        "regex": r"^[A-Z\d]+-[A-Z\d]+$",
    },
    "alias": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "nnd_model_version": {"type": "integer", "required": True},
    "categories": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {"name": {"type": "string", "required": True}},
        },
    },
    "type": {"allowed": ["shared_object_type"], "required": True},
    "parameters": {
        "type": "list",
        "schema": {
            "type": "dict",
            "anyof_schema": [
                parameter_field_schema.copy(),
                parameter_group_schema.copy(),
            ],
        },
    },
}
connection_type_schema = {
    "uuid": {
        "type": "string",
        "minlength": 8,
        "required": True,
        "regex": r"^[A-Z\d]+-[A-Z\d]+$",
    },
    "alias": {"type": "string", "required": True},
    "description": {"type": "string", "required": True},
    "nnd_model_version": {"type": "integer", "required": True},
    "categories": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {"name": {"type": "string", "required": True}},
        },
    },
    "type": {"allowed": ["connection"], "required": True},
    "parameters": {
        "type": "list",
        "schema": {"type": "dict", "schema": parameter_group_schema.copy()},
    },
}
schemas = {
    "engine": engine_schema,
    "shared_object_type": shared_object_type_schema,
    "connection": connection_type_schema,
}


def validate_model(model):
    schema = schemas[model["type"]]
    validator = Validator(schema)
    if not validator.validate(model):
        _logger.error(
            f"Errors validating {model['type']} model \n\t\t{pformat(validator.errors)}"
        )
        return False
    else:
        return True
