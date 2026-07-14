import json
import os
import re
import uuid
from pathlib import Path


TRACE_ID = re.compile(r"^[0-9a-f]{32}$")


class TraceService:
    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex

    def _path(self, trace_id: str) -> Path:
        if not TRACE_ID.fullmatch(trace_id):
            raise ValueError("Trace ID không hợp lệ.")
        return self.directory / f"{trace_id}.json"

    def save(self, trace: dict) -> None:
        path = self._path(trace["trace_id"])
        temporary = path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(trace, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        os.replace(temporary, path)

    def get(self, trace_id: str) -> dict | None:
        try:
            path = self._path(trace_id)
        except ValueError:
            return None
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def clear(self) -> int:
        traces = [path for path in self.directory.glob("*.json") if TRACE_ID.fullmatch(path.stem)]
        for path in traces:
            path.unlink(missing_ok=True)
        return len(traces)

