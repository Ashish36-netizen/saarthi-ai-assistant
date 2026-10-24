from ollama import Client


class LLMBrain:
    """Handles AI responses using Ollama (local LLM)."""

    def __init__(self, model="llama3.2:3b", host="http://localhost:11434"):
        self.model = model
        self.client = Client(host=host)
        print(f"[LLM] Initialized with model: {model}")

    def is_available(self):
        """Check if Ollama is running and model is available."""
        try:
            models = self.client.list()
            model_names = [m["model"] for m in models.get("models", [])]
            return any(self.model in name for name in model_names)
        except Exception as e:
            print(f"[LLM] Ollama not available: {e}")
            return False

    def generate_response(self, user_text, system_prompt=None):
        """Generate AI response for user input."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_text})

        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.7,
                    "num_predict": 200,  # max tokens (short answers)
                },
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(f"[LLM] Error: {e}")
            return None