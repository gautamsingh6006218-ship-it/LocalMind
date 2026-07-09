import os

# Falls back to these defaults if not set in .env - lets you override
# any of these without touching code, just by editing .env.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
# Low temperature favors direct, consistent, fact-stating answers over creative
# paraphrasing - matters for a grounded RAG assistant more than for open-ended chat.
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "localmind")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
