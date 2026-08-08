import json

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from tests.test_harness import CONTRACTS_DIR, EXAMPLES_DIR


def load_schema():
    return json.loads(
        (CONTRACTS_DIR / "knowledge-manifest.schema.json").read_text(encoding="utf-8")
    )


def test_schema_is_valid_draft_2020_12():
    Draft202012Validator.check_schema(load_schema())


def test_example_validates():
    example = json.loads(
        (EXAMPLES_DIR / "knowledge-manifest.example.json").read_text(encoding="utf-8")
    )
    validate(example, load_schema())


def test_embeddings_key_rejected():
    example = json.loads(
        (EXAMPLES_DIR / "knowledge-manifest.example.json").read_text(encoding="utf-8")
    )
    example["embeddings"] = {"model": "nomic-embed-text", "vectors": []}
    with pytest.raises(ValidationError):
        validate(example, load_schema())
