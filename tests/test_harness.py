from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = REPO_ROOT / "contracts"
EXAMPLES_DIR = REPO_ROOT / "examples"


def test_contract_dirs_exist():
    assert CONTRACTS_DIR.is_dir(), "contracts/ missing"
    assert EXAMPLES_DIR.is_dir(), "examples/ missing"
