import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from modules.config_loader import load_config
from modules.voice_engine.stt import SpeechToText
from modules.voice_engine.tts import TextToSpeech
from modules.ai_brain.llm import LLMBrain
from modules.ai_brain.memory import ConversationMemory
from modules.ai_brain.prompts import SAARTHI_SYSTEM_PROMPT


def main():
    config = load_config()
    assistant_name = config["assistant"]["name"]

    stt = SpeechToText(
        model_size=config["stt"]["model_size"],
        device=config["stt"]["device"],
        compute_type=config["stt"]["compute_type"],
    )
    tts = TextToSpeech(voice=config["tts"]["voice"])

    brain = LLMBrain(model="llama3.2:3b")
    if not brain.is_available():
        print("[MAIN] Warning: Ollama not available. Falling back to echo mode.")

    memory = ConversationMemory(max_messages=10)

    tts.speak(f"Namaste! Main {assistant_name} hoon. Boliye, kya jaanna hai?")

    while True:
        audio = stt.record_audio(duration=5)
        text = stt.transcribe(audio)

        cleaned = text.strip().strip(".!? ,")
        if not cleaned or len(cleaned) < 3:
            print("[MAIN] Kuch sunai nahi diya, dobara try karo.")
            continue

        word_count = len(cleaned.split())
        if word_count == 1 and len(cleaned) < 5:
            print("[MAIN] Samajh nahi aaya, dobara bolo.")
            continue

        print(f"\n[USER]: {text}")

        # Reset command
        lower_text = text.lower().strip().strip(".!? ,")
        if any(word in lower_text for word in ["reset", "clear memory", "naya session", "memory clear"]):
            print("[MAIN] Memory reset requested.")
            memory.clear()
            tts.speak("Memory clear ho gayi. Naya session shuru.")
            print("[MAIN] Memory cleared successfully.")
            continue

        # Exit commands
        if any(word in text.lower() for word in ["exit", "stop", "band", "bye", "goodbye"]):
            tts.speak("Dhanyavaad! Phir milenge.")
            break

        # AI Response with memory
        print("[SAARTHI] Soch raha hoon...")
        response = brain.generate_response(
            text,
            system_prompt=SAARTHI_SYSTEM_PROMPT,
            memory=memory,
        )

        if response:
            print(f"[SAARTHI]: {response}")
            tts.speak(response)

            # Save to memory AFTER successful response
            memory.add_user(text)
            memory.add_assistant(response)
        else:
            tts.speak("Sorry, main abhi jawab nahi de paya. Dobara try karo.")


if __name__ == "__main__":
    main()