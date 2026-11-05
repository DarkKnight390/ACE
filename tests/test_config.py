import os
import unittest
from unittest.mock import patch

from ace_voice.config import Settings


class SettingsTests(unittest.TestCase):
    def test_defaults_to_local_faster_whisper_cpu(self) -> None:
        env = {
            "ACE_NVIDIA_API_KEY": "nvidia-test",
            "ACE_NVIDIA_MODEL": "test-model",
            "ACE_ELEVENLABS_API_KEY": "eleven-test",
            "ACE_ELEVENLABS_VOICE_ID": "voice-test",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_env()

        self.assertEqual(settings.stt_model, "small")
        self.assertEqual(settings.stt_device, "cpu")
        self.assertEqual(settings.stt_compute_type, "int8")
        self.assertIsNone(settings.stt_language)

    def test_accepts_faster_whisper_runtime_configuration(self) -> None:
        env = {
            "ACE_NVIDIA_API_KEY": "nvidia-test",
            "ACE_NVIDIA_MODEL": "test-model",
            "ACE_ELEVENLABS_API_KEY": "eleven-test",
            "ACE_ELEVENLABS_VOICE_ID": "voice-test",
            "ACE_STT_MODEL": "large-v3",
            "ACE_STT_DEVICE": "cuda",
            "ACE_STT_COMPUTE_TYPE": "float16",
            "ACE_STT_LANGUAGE": "en",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_env()

        self.assertEqual(settings.stt_model, "large-v3")
        self.assertEqual(settings.stt_device, "cuda")
        self.assertEqual(settings.stt_compute_type, "float16")
        self.assertEqual(settings.stt_language, "en")


if __name__ == "__main__":
    unittest.main()
