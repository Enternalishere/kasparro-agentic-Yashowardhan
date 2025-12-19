import json
import time
from pathlib import Path
from typing import Dict, Any, Iterator
from contextlib import contextmanager
from config import LOG_PATH


def log_event(event: Dict[str, Any]) -> None:
    Path(Path(LOG_PATH).parent).mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


@contextmanager
def agent_span(name: str, extra: Dict[str, Any] | None = None) -> Iterator[None]:
    start = time.time()
    log_event({"type": "agent_start", "name": name, "ts": start, "extra": extra or {}})
    try:
        yield
        end = time.time()
        log_event({"type": "agent_end", "name": name, "ts": end, "latency_ms": int((end - start) * 1000)})
    except Exception as e:
        end = time.time()
        log_event({
            "type": "agent_error",
            "name": name,
            "ts": end,
            "latency_ms": int((end - start) * 1000),
            "error": str(e),
        })
        raise
