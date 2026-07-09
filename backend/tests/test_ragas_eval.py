import pytest
from app.eval.ragas_eval import score_faithfulness


@pytest.mark.asyncio
async def test_score_faithfulness_returns_value_between_0_and_1():
    score = await score_faithfulness(
        question="What color is the sky?",
        contexts=["The sky is blue on a clear day due to Rayleigh scattering."],
        answer="The sky is blue.",
    )
    assert 0.0 <= score <= 1.0


@pytest.mark.asyncio
async def test_faithful_answer_scores_higher_than_hallucinated_one():
    faithful_score = await score_faithfulness(
        question="What color is the sky?",
        contexts=["The sky is blue on a clear day due to Rayleigh scattering."],
        answer="The sky is blue.",
    )
    hallucinated_score = await score_faithfulness(
        question="What color is the sky?",
        contexts=["The sky is blue on a clear day due to Rayleigh scattering."],
        answer="The sky is purple with green stripes.",
    )
    assert faithful_score > hallucinated_score
