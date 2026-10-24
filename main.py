import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from modules.config_loader import load_config
from modules.voice_engine.stt import SpeechToText
from modules.voice_engine.tts import TextToSpeech
from modules.ai_brain.llm import LLMBrain
from modules.ai_brain.prompts import SAARTHI_SYSTEM_PROMPT


def main():
    config = load_config()
    assistant_name = config["assistant"]["name"]

    # Initialize modules
    stt = SpeechToText(
        model_size=config["stt"]["model_size"],
        device=config["stt"]["device"],
        compute_type=config["stt"]["compute_type"],
    )
    tts = TextToSpeech(voice=config["tts"]["voice"])

    # Initialize AI Brain
    brain = LLMBrain(model="llama3.2:3b")
    if not brain.is_available():
        print("[MAIN] Warning: Ollama not available. Falling back to echo mode.")

    # Greeting
    tts.speak(f"Namaste! Main {assistant_name} hoon. Boliye, kya jaanna hai?")

    # Conversation loop
    while True:
        audio = stt.record_audio(duration=5)
        text = stt.transcribe(audio)

        # Filter silence/noise
        # Strict filter: reject very short or gibberish text
        cleaned = text.strip().strip(".!? ,")
        if not cleaned or len(cleaned) < 3:
            print("[MAIN] Kuch sunai nahi diya, dobara try karo.")
            continue

        # Reject text that's only punctuation or single random words
        word_count = len(cleaned.split())
        if word_count == 1 and len(cleaned) < 5:
            print("[MAIN] Samajh nahi aaya, dobara bolo.")
            continue

        print(f"\n[USER]: {text}")

        # Exit commands
        if any(word in text.lower() for word in ["exit", "stop", "band", "bye", "goodbye"]):
            tts.speak("Dhanyavaad! Phir milenge.")
            break

        # AI Response
        print("[SAARTHI] Soch raha hoon...")
        response = brain.generate_response(text, system_prompt=SAARTHI_SYSTEM_PROMPT)

        if response:
            print(f"[SAARTHI]: {response}")
            tts.speak(response)
        else:
            # Fallback if LLM fails
            tts.speak("Sorry, main abhi jawab nahi de paya. Dobara try karo.")


if __name__ == "__main__":
    main()