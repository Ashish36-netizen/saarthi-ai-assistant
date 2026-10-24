import yaml
from pathlib import Path

def load_config(path="config.yaml"):
    """Load configuration from YAML file."""
    config_path = Path(__file__).parent.parent / path
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config = load_config()
    print("Config loaded successfully:")
    print(f"  Assistant name: {config['assistant']['name']}")
    print(f"  Wake word: {config['assistant']['wake_word']}")
    print(f"  STT model: {config['stt']['model_size']}")