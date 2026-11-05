from __future__ import annotations

import re


_SENTENCE_END = re.compile(r"""[.!?]["'’”)]*\s+""")


class PhraseSegmenter:
    def __init__(self, max_chars: int = 180, min_split_chars: int = 80) -> None:
        if min_split_chars < 1 or max_chars <= min_split_chars:
            raise ValueError("Phrase limits must satisfy 1 <= min_split_chars < max_chars")
        self._buffer = ""
        self._max_chars = max_chars
        self._min_split_chars = min_split_chars

    def feed(self, text: str) -> list[str]:
        self._buffer += text
        phrases: list[str] = []
        while self._buffer:
            sentence_end = _SENTENCE_END.search(self._buffer)
            if sentence_end is not None:
                phrase = self._buffer[: sentence_end.end()].strip()
                self._buffer = self._buffer[sentence_end.end() :]
                if phrase:
                    phrases.append(phrase)
                continue

            if len(self._buffer) < self._max_chars:
                break
            split_at = self._buffer.rfind(" ", self._min_split_chars, self._max_chars)
            if split_at < self._min_split_chars:
                break
            phrase = self._buffer[:split_at].strip()
            self._buffer = self._buffer[split_at + 1 :]
            if phrase:
                phrases.append(phrase)
        return phrases

    def flush(self) -> list[str]:
        phrase = self._buffer.strip()
        self._buffer = ""
        return [phrase] if phrase else []
