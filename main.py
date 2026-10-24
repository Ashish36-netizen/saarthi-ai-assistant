import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from modules.config_loader import load_config
from modules.voice_engine.stt import SpeechToText
from modules.voice_engine.tts import TextToSpeech
from modules.config_loader import load_config
from modules.voice_engine.stt import SpeechToText
from modules.voice_engine.tts import TextToSpeech


def main():
    # Load config
    config = load_config()
    assistant_name = config["assistant"]["name"]

    # Initialize modules
    stt = SpeechToText(
        model_size=config["stt"]["model_size"],
        device=config["stt"]["device"],
        compute_type=config["stt"]["compute_type"],
    )
    tts = TextToSpeech(voice=config["tts"]["voice"])

    # Greeting
    tts.speak(f"Namaste! Main {assistant_name} hoon. Boliye, kya karna hai?")

    # Conversation loop
    while True:
        audio = stt.record_audio(duration=5)
        text = stt.transcribe(audio)

        # Filter out silence/noise (empty text or only punctuation)
        cleaned = text.strip().strip(".!? ,")
        if not cleaned or len(cleaned) < 2:
            print("[MAIN] Kuch sunai nahi diya, dobara try karo.")
            continue

        print(f"\n[USER]: {text}")

        # Exit commands
        if any(word in text.lower() for word in ["exit", "stop", "band", "bye", "goodbye"]):
            tts.speak("Dhanyavaad! Phir milenge.")
            break

        # Echo reply (Week 2 mein ise LLM se replace karenge)
        tts.speak(f"Aapne kaha: {text}")


if __name__ == "__main__":
    main()