import json

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from tests.test_harness import CONTRACTS_DIR, EXAMPLES_DIR


def load_schema():
    return json.loads((CONTRACTS_DIR / "workload-identity.schema.json").read_text())


def test_schema_is_valid_draft_2020_12():
    Draft202012Validator.check_schema(load_schema())


@pytest.mark.parametrize("name", [
    "workload-identity.bearer.example.json",
    "workload-identity.x509.example.json",
])
def test_examples_validate(name):
    example = json.loads((EXAMPLES_DIR / name).read_text())
    validate(example, load_schema())


def test_x509_requires_spiffe_id():
    bad = {
        "principal_type": "agent",
        "id": "billing-agent",
        "issuer": "https://agentprint.example.com",
        "credential": {"type": "x509-svid", "x509": {}},
    }
    with pytest.raises(ValidationError):
        validate(bad, load_schema())


def test_unknown_principal_type_rejected():
    bad = {
        "principal_type": "robot",
        "id": "x",
        "issuer": "https://agentprint.example.com",
        "credential": {"type": "bearer-token"},
    }
    with pytest.raises(ValidationError):
        validate(bad, load_schema())
