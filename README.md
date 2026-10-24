@"
# SAARTHI

**Smart AI Assistant for Real-Time Help & Interaction**

> *Aapka Digital Saarthi*

SAARTHI is an AI-powered desktop voice assistant built with Python. It listens to your voice commands, understands them using a local LLM, and performs tasks on your computer - all while keeping your data private and offline-first.

## Features

- Voice Control - Wake word detection + speech-to-text + text-to-speech
- AI Brain - Powered by Ollama (Llama 3.2) for intelligent conversations
- OS Automation - Open apps, control volume, take screenshots, and more
- Communication - Send WhatsApp messages and emails via voice
- Document Q&A - Ask questions about your PDFs (RAG)
- Privacy-First - Local LLM + offline mode, no data leaves your system
- Modern GUI - CustomTkinter dashboard with live status

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| Speech-to-Text | Faster-Whisper |
| Text-to-Speech | edge-tts + pyttsx3 (fallback) |
| Wake Word | openWakeWord |
| LLM | Ollama + Llama 3.2 |
| Agentic AI | LangGraph |
| RAG | LangChain + ChromaDB |
| Automation | pyautogui, psutil |
| GUI | CustomTkinter |

## Project Status

Under Development - B.Tech Minor Project (Final Year)

## Author

Ashish Bhonsle
- GitHub: [@Ashish36-netizen](https://github.com/Ashish36-netizen)

---

If you find this project interesting, give it a star!
"@ | Out-File -FilePath README.md -Encoding utf8