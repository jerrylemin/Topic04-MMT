import inspect

from scripts import run_runtime_smoke_test as smoke


def test_runtime_smoke_target_is_fixed_loopback():
    assert smoke.BASE_URL == "http://127.0.0.1:5005"


def test_runtime_smoke_has_no_configurable_target_argument():
    source = inspect.getsource(smoke)
    assert "argparse" not in source
    assert "sys.argv" not in source
    assert "input(" not in source


def test_runtime_smoke_checks_required_fixed_flows():
    source = inspect.getsource(smoke.main)
    for label in (
        "Healthcheck", "Home", "Normal vulnerable login", "Fixed local authentication logic demo",
        "Secure login rejects same input", "Normal secure login", "Normal vulnerable search",
        "Expanded vulnerable product search", "Secure search preserves structure",
        "Secure user detail", "Security headers",
    ):
        assert label in source


def test_runtime_smoke_log_path_is_inside_lab_evidence():
    assert smoke.LOG.name == "runtime_smoke_test.txt"
    assert smoke.LOG.parent.name == "logs"
    assert smoke.LOG.parent.parent.name == "evidence"

