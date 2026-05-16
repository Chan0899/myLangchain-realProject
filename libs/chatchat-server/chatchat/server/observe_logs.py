from __future__ import annotations

import json
import threading
from datetime import datetime
from pathlib import Path

from chatchat.settings import Settings


_WRITE_LOCK = threading.Lock()


def _local_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _daily_log_file(log_type: str, filename_prefix: str) -> Path:
    day = datetime.now().strftime("%Y%m%d")
    return (
        Settings.basic_settings.DATA_PATH
        / "observe_logs"
        / log_type
        / f"{filename_prefix}_{day}.jsonl"
    )


def _append_jsonl(log_file: Path, payload: dict) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, ensure_ascii=False)
    with _WRITE_LOCK:
        with log_file.open("a", encoding="utf-8") as file:
            file.write(f"{line}\n")


def log_query_event(query_id: str) -> None:
    _append_jsonl(
        _daily_log_file("query", "query_logs"),
        {
            "timestamp": _local_timestamp(),
            "query_id": query_id,
        },
    )


def log_ingest_event(doc_id: str) -> None:
    _append_jsonl(
        _daily_log_file("ingest", "ingest_logs"),
        {
            "timestamp": _local_timestamp(),
            "doc_id": doc_id,
        },
    )