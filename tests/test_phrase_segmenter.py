import unittest

from ace_voice.phrase_segmenter import PhraseSegmenter


class PhraseSegmenterTests(unittest.TestCase):
    def test_splits_complete_sentences_across_chunks(self) -> None:
        segmenter = PhraseSegmenter()
        self.assertEqual(segmenter.feed("Hello there. How"), ["Hello there."])
        self.assertEqual(segmenter.feed(" can I help?"), [])
        self.assertEqual(segmenter.flush(), ["How can I help?"])

    def test_splits_overlong_text_at_a_word_boundary(self) -> None:
        segmenter = PhraseSegmenter(max_chars=30, min_split_chars=12)
        text = "one two three four five six seven eight nine"
        phrases = segmenter.feed(text)
        phrases.extend(segmenter.flush())
        self.assertEqual(" ".join(phrases), text)
        self.assertTrue(all(len(phrase) < 30 for phrase in phrases))

    def test_rejects_invalid_limits(self) -> None:
        with self.assertRaises(ValueError):
            PhraseSegmenter(max_chars=10, min_split_chars=10)


if __name__ == "__main__":
    unittest.main()
