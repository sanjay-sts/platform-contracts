import pytest
import yaml
from openapi_spec_validator import validate as validate_openapi

from tests.test_harness import CONTRACTS_DIR

OPENAPI_FILES = [
    "registry-sync.openapi.yaml",
    "deploy-push.openapi.yaml",
]


@pytest.mark.parametrize("name", OPENAPI_FILES)
def test_openapi_spec_is_valid(name):
    spec = yaml.safe_load((CONTRACTS_DIR / name).read_text(encoding="utf-8"))
    validate_openapi(spec)


def test_registry_sync_covers_all_object_types():
    spec = yaml.safe_load(
        (CONTRACTS_DIR / "registry-sync.openapi.yaml").read_text(encoding="utf-8")
    )
    enum = spec["components"]["schemas"]["ObjectType"]["enum"]
    assert sorted(enum) == sorted(
        ["agent", "mcp-server", "skill", "prompt", "app", "policy", "knowledge-bundle"]
    )


def test_deploy_status_enum():
    spec = yaml.safe_load(
        (CONTRACTS_DIR / "deploy-push.openapi.yaml").read_text(encoding="utf-8")
    )
    enum = spec["components"]["schemas"]["Deployment"]["properties"]["status"]["enum"]
    assert enum == ["queued", "building", "deployed", "failed"]
