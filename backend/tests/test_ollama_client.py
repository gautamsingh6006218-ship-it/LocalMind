from app.llm.ollama_client import generate_answer


def test_generate_answer_returns_non_empty_string():
    answer = generate_answer(
        question="What color is the sky?",
        context="The sky is blue on a clear day due to Rayleigh scattering.",
    )

    assert isinstance(answer, str)
    assert len(answer) > 0


def test_generate_answer_uses_context_when_relevant():
    # Loose check, not exact-text - LLM phrasing varies between runs.
    # If the context clearly states the answer, the model's response should
    # reference it (here: mention "blue"), not go silent or say it doesn't know.
    answer = generate_answer(
        question="What color is the sky?",
        context="The sky is blue on a clear day due to Rayleigh scattering.",
    )

    assert "blue" in answer.lower()


def test_generate_answer_admits_when_context_is_irrelevant():
    # When the context has nothing to do with the question, the prompt
    # instructs the model to say so rather than hallucinate an answer.
    answer = generate_answer(
        question="What is the capital of France?",
        context="Bananas are a good source of potassium and fiber.",
    )

    assert "don't know" in answer.lower() or "doesn't contain" in answer.lower() or "not" in answer.lower()
