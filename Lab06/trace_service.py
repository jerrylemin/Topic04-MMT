from __future__ import annotations

import json
import threading
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any

from security_utils import generate_trace_id, isoformat_utc, redact, utc_now
from trace_models import FinalVerdict, TraceRecord, TraceStep


class TraceStore:
    def __init__(self, max_items: int = 256) -> None:
        self._max_items = max_items
        self._items: OrderedDict[str, TraceRecord] = OrderedDict()
        self._lock = threading.RLock()

    def put(self, trace: TraceRecord) -> None:
        with self._lock:
            self._items[trace.trace_id] = trace
            self._items.move_to_end(trace.trace_id)
            while len(self._items) > self._max_items:
                self._items.popitem(last=False)

    def get(self, trace_id: str) -> TraceRecord | None:
        with self._lock:
            return self._items.get(trace_id)

    def clear(self) -> int:
        with self._lock:
            count = len(self._items)
            self._items.clear()
            return count


TRACE_STORE = TraceStore()


def begin_trace(
    *, mode: str, route: str, now: datetime | None = None, trace_id: str | None = None
) -> TraceRecord:
    trace = TraceRecord(
        trace_id=trace_id or generate_trace_id(),
        mode=mode,
        route=route,
        started_at=isoformat_utc(now or utc_now()),
    )
    TRACE_STORE.put(trace)
    return trace


def add_step(
    trace: TraceRecord,
    *,
    layer: str,
    title: str,
    description: str,
    technique: str,
    input_data: Any,
    output_data: Any,
    code_reference: str,
    security_meaning: str,
    status: str,
    now: datetime | None = None,
) -> TraceStep:
    step = TraceStep(
        step_number=len(trace.steps) + 1,
        timestamp=isoformat_utc(now or utc_now()),
        layer=layer,
        title=title,
        description=description,
        technique=technique,
        input_data=redact(input_data),
        output_data=redact(output_data),
        code_reference=code_reference,
        security_meaning=security_meaning,
        status=status,
    )
    trace.steps.append(step)
    TRACE_STORE.put(trace)
    return step


def finish_trace(
    trace: TraceRecord,
    *,
    status: str,
    verdict: FinalVerdict,
    now: datetime | None = None,
) -> TraceRecord:
    trace.status = status
    trace.completed_at = isoformat_utc(now or utc_now())
    trace.verdict = verdict
    TRACE_STORE.put(trace)
    return trace


def get_trace(trace_id: str) -> TraceRecord | None:
    return TRACE_STORE.get(trace_id)


def clear_traces() -> int:
    return TRACE_STORE.clear()


def export_trace(trace: TraceRecord, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(trace.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return destination


def sanitize_trace_value(name: str, value: object) -> object:
    return redact(value, field_name=name)
