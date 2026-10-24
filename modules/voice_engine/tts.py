import asyncio
import os
import pyttsx3
import pygame


class TextToSpeech:
    """Handles text-to-speech with online (edge-tts) and offline (pyttsx3) fallback."""

    def __init__(self, voice="en-US-JennyNeural"):
        self.voice = voice
        self.offline_engine = pyttsx3.init()
        self.offline_engine.setProperty("rate", 175)
        pygame.mixer.init()
        print("[TTS] Initialized.")

    def speak(self, text):
        """Try online TTS first, fallback to offline if it fails."""
        try:
            asyncio.run(self._speak_online(text))
        except Exception as e:
            print(f"[TTS] Online failed ({e}), using offline fallback.")
            self._speak_offline(text)

    async def _speak_online(self, text):
        import edge_tts
        communicate = edge_tts.Communicate(text, self.voice)
        temp_file = "temp_reply.mp3"
        await communicate.save(temp_file)

        if not os.path.exists(temp_file) or os.path.getsize(temp_file) < 1000:
            raise Exception("Empty or invalid audio file generated")

        # Play with pygame — blocks until playback finishes
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()

        try:
            os.remove(temp_file)
        except OSError:
            pass

    def _speak_offline(self, text):
        self.offline_engine.say(text)
        self.offline_engine.runAndWait()