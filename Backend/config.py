import os

class Settings:
    PORT: int = int(os.getenv("PORT", "7860"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "heuristic")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

settings = Settings()
