import json
from datetime import datetime
from types import SimpleNamespace

from chatchat.server import observe_logs


def test_observe_logs_write_daily_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(
        observe_logs,
        "Settings",
        SimpleNamespace(basic_settings=SimpleNamespace(DATA_PATH=tmp_path)),
    )

    observe_logs.log_query_event("q001")
    observe_logs.log_ingest_event("rtx4090.pdf")

    day = datetime.now().strftime("%Y%m%d")
    query_log = tmp_path / "observe_logs" / "query" / f"query_logs_{day}.jsonl"
    ingest_log = tmp_path / "observe_logs" / "ingest" / f"ingest_logs_{day}.jsonl"

    assert query_log.exists()
    assert ingest_log.exists()

    query_payload = json.loads(query_log.read_text(encoding="utf-8").strip())
    ingest_payload = json.loads(ingest_log.read_text(encoding="utf-8").strip())

    assert query_payload["query_id"] == "q001"
    assert ingest_payload["doc_id"] == "rtx4090.pdf"
    assert datetime.strptime(query_payload["timestamp"], "%Y-%m-%dT%H:%M:%S")
    assert datetime.strptime(ingest_payload["timestamp"], "%Y-%m-%dT%H:%M:%S")