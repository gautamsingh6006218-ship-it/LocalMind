import ollama


def generate_answer(question: str, context: str) -> str:
    """Ask the local Llama model to answer `question`, grounded only in `context`."""
    # Explicitly instructing the model to answer using only the given context -
    # and to admit when it can't - is what makes this a grounded RAG answer
    # instead of a generic answer from the model's own training data.
    prompt = f"""Answer the following question based on the provided context. If the context doesn't contain the answer, say "Sorry, I don't know".

    Context: {context}
    Question: {question}
    """

    # Sends the prompt to the Ollama container and waits for the full response
    # (not streamed - the whole answer comes back in one call).
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
    )

    return response["message"]["content"]
