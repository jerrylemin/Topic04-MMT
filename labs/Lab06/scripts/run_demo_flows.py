"""Run the fixed Lab06 Flask test-client scenarios without external requests."""

from __future__ import annotations

import json

from export_evidence import run_fixed_flows


def main() -> int:
    _app, captures = run_fixed_flows()
    observed = {
        capture.name: {
            "status_code": capture.response["status_code"],
            "decision": capture.response["decision"],
            "trace_id": capture.trace["trace_id"],
        }
        for capture in captures
    }
    print(json.dumps(observed, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Observed {len(captures)} fixed local flow(s); no evidence files were written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
