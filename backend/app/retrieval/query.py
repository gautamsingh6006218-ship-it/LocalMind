from app.embeddings.embedder import embed_text
from app.retrieval.retriever import search
from app.llm.ollama_client import generate_answer

# Standalone script kept for quick manual testing from the command line -
# now reuses the same modules the /chat API endpoint uses, instead of
# duplicating the embedding/search/generation logic here.

question = "What is the best ways to distribute wealth?"

query_vector = embed_text(question)
matches = search(query_vector, limit=3)
context = "\n\n".join(match["text"] for match in matches)
answer = generate_answer(question, context)

print("\nAnswer:", answer)
