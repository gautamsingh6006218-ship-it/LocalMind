import os

# model used to generate chat answers
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
# low = more direct/factual, less random
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))
# address of the Qdrant vector database
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# name of the collection storing document chunks
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "localmind")
# model that turns text into vectors
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")

# bigger model used only to judge answer quality
# RAGAS_JUDGE_MODEL = os.getenv("RAGAS_JUDGE_MODEL", "llama3.1:8b")
RAGAS_JUDGE_MODEL = os.getenv("RAGAS_JUDGE_MODEL", "qwen2.5:7b")

# Ollama's OpenAI-compatible endpoint
OLLAMA_OPENAI_BASE_URL = os.getenv("OLLAMA_OPENAI_BASE_URL", "http://localhost:11434/v1")

# fraction of chat requests that get RAGAS-scored, to reduce Ollama resource contention
RAGAS_SAMPLE_RATE = float(os.getenv("RAGAS_SAMPLE_RATE", "0.33"))
