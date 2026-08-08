import json

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from tests.test_harness import CONTRACTS_DIR, EXAMPLES_DIR


def load_schema():
    return json.loads((CONTRACTS_DIR / "tags.schema.json").read_text())


def test_schema_is_valid_draft_2020_12():
    Draft202012Validator.check_schema(load_schema())


def test_example_validates():
    example = json.loads((EXAMPLES_DIR / "tags.example.json").read_text())
    validate(example, load_schema())


@pytest.mark.parametrize("bad", [
    ["Risk:destructive"],        # uppercase namespace
    ["risk destructive"],        # no colon
    ["risk:"],                   # empty value
    [":destructive"],            # empty namespace
    ["risk:readonly", "risk:readonly"],  # duplicates
])
def test_invalid_tag_sets_rejected(bad):
    with pytest.raises(ValidationError):
        validate(bad, load_schema())
