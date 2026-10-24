from modules.voice_engine.stt import SpeechToText

stt = SpeechToText(model_size="tiny")
audio = stt.record_audio(duration=4)
text = stt.transcribe(audio)
print(f"\n[RESULT] Aapne kaha: {text}")