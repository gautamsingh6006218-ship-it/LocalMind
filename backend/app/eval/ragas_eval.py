from ragas import SingleTurnSample
from ragas.metrics import Faithfulness
from ragas.llms import LangchainLLMWrapper
from langchain_ollama import ChatOllama

from app.config import OLLAMA_MODEL

# Wraps our local Ollama model in RAGAS's expected LangChain interface -
# this is what keeps RAGAS's scoring fully offline instead of defaulting to OpenAI.
_judge_llm = LangchainLLMWrapper(ChatOllama(model=OLLAMA_MODEL))
_faithfulness = Faithfulness(llm=_judge_llm)


async def score_faithfulness(question: str, contexts: list[str], answer: str) -> float:
    """Score how well `answer`'s claims are supported by `contexts` (0-1, higher = more faithful)."""
    sample = SingleTurnSample(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts,
    )
    return await _faithfulness.single_turn_ascore(sample)
