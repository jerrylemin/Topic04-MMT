from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_smoke_script_is_fixed_to_loopback_and_covers_required_flows():
    source = (ROOT / "scripts/run_runtime_smoke_test.py").read_text(encoding="utf-8")
    assert "argparse" not in source and "sys.argv" not in source
    assert 'VICTIM = "http://127.0.0.1:5004"' in source
    assert 'DEMO = "http://127.0.0.1:9004"' in source
    for flow in ("Healthcheck Victim", "Healthcheck Demo Page", "Login victim", "Vulnerable email change", "Reset valid token", "Secure email missing token", "Secure email invalid token", "Secure email Origin denied", "Secure email success", "Logout missing token", "Logout success"):
        assert flow in source
    assert "SameSite/SOP browser claim" in source
