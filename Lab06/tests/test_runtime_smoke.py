from __future__ import annotations

import inspect

from scripts import run_runtime_smoke_test


def test_smoke_runner_has_one_fixed_loopback_target_and_no_cli_target_input():
    source = inspect.getsource(run_runtime_smoke_test)
    assert run_runtime_smoke_test.BASE_URL == "http://127.0.0.1:5006"
    assert "argparse" not in source
    assert "sys.argv" not in source


def test_smoke_runner_emits_explicit_report_success_marker():
    source = inspect.getsource(run_runtime_smoke_test.main)
    assert "SMOKE_TEST_PASSED" in source
