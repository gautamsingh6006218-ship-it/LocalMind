import sys
import types

# creates an empty fake module
_stub = types.ModuleType("langchain_community.chat_models.vertexai")
# adds an empty placeholder class into it
_stub.ChatVertexAI = type("ChatVertexAI", (), {})
# registers the fake module so ragas's broken import finds it
sys.modules["langchain_community.chat_models.vertexai"] = _stub


from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import Faithfulness

from app.config import RAGAS_JUDGE_MODEL, OLLAMA_OPENAI_BASE_URL


# points the client at local Ollama, not OpenAI's servers
_client = AsyncOpenAI(base_url=OLLAMA_OPENAI_BASE_URL, api_key="ollama")
# wraps our local model as a ragas-compatible judge
_judge_llm = llm_factory(RAGAS_JUDGE_MODEL, provider="openai", client=_client)
# the scorer object, created once at import time
_faithfulness = Faithfulness(llm=_judge_llm)


async def score_faithfulness(question: str, contexts: list[str], answer: str) -> float:
    """Score how well `answer`'s claims are supported by `contexts` (0-1, higher = more faithful)."""
    # asks the judge model to score this question/answer/context
    result = await _faithfulness.ascore(
        # the original question
        user_input=question,
        # the answer our chat model generated
        response=answer,
        # the chunks retrieved from Qdrant
        retrieved_contexts=contexts,
    )
    # pulls just the numeric score (0-1) out of the result object
    return result.value
