from __future__ import annotations

from ckan.logic.schema import validator_args


@validator_args
def query_popularity_import(not_empty, boolean_validator, convert_to_json_if_string):
    return {
        "snapshot": [not_empty, convert_to_json_if_string],
        "reset": [boolean_validator],
    }
