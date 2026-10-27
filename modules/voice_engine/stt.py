import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


class SpeechToText:
    """Handles speech-to-text conversion using Faster-Whisper."""

    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        print(f"[STT] Loading Whisper model: {model_size}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.samplerate = 16000
        print("[STT] Model loaded successfully.")

    def record_audio(self, duration=5):
        """Record audio from the microphone for `duration` seconds."""
        print(f"[STT] Listening for {duration} seconds...")
        audio = sd.rec(
            int(duration * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        print("[STT] Recording complete.")
        return np.squeeze(audio)

    def transcribe(self, audio):
        """Convert audio to text with VAD and noise filtering."""
        segments, info = self.model.transcribe(
            audio,
            beam_size=5,
            language=None,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
        )

        # Only reject clearly non-speech languages (not Hinglish misdetections)
        if info.language not in ("en", "hi", "ur", "bn"):
            print(f"[STT] Rejected - detected language: {info.language}")
            return ""

        # Only reject segments with low speech probability
        valid_segments = [seg for seg in segments if seg.no_speech_prob < 0.6]
        text = " ".join(seg.text for seg in valid_segments).strip()
        return text