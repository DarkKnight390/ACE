from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path


class JsonlSessionLogger:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = asyncio.Lock()

    async def record(
        self,
        session_id: str,
        event: str,
        metadata: Mapping[str, str | int | float | bool | None],
    ) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "event": event,
            "metadata": dict(metadata),
        }
        line = json.dumps(record, separators=(",", ":"), ensure_ascii=True) + "\n"
        async with self._lock:
            await asyncio.to_thread(self._append, line)

    def _append(self, line: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8", newline="\n") as log_file:
            log_file.write(line)
