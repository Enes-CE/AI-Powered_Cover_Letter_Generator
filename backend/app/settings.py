import os


class Settings:
    AI_PROVIDER = os.getenv("AI_PROVIDER", "template")  # ollama | openai | template
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct")
    AI_TIMEOUT = float(os.getenv("AI_TIMEOUT", "30"))


settings = Settings()


