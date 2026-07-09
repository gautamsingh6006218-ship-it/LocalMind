from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from langfuse import observe, get_client
from app.embeddings.embedder import embed_text
from app.llm.ollama_client import generate_answer
from app.retrieval.retriever import search
from app.eval.ragas_eval import score_faithfulness

# groups all routes defined in this file
router = APIRouter()


class ChatRequest(BaseModel):
    # the question sent by the client
    question: str


class ChatResponse(BaseModel):
    # the answer sent back to the client
    answer: str


async def _score_and_log(trace_id: str, question: str, contexts: list[str], answer: str):
    # runs RAGAS scoring - this happens after the response was already sent
    score = await score_faithfulness(question, contexts, answer)
    # attaches the score to the original trace, found by its ID
    get_client().create_score(
        trace_id=trace_id,
        name="faithfulness",
        value=score,
        data_type="NUMERIC",
    )
    # sends the buffered score data to Langfuse immediately
    get_client().flush()


# registers this function to handle POST requests to /chat
@router.post("/chat")
# wraps this function in a Langfuse trace named "chat_query"
@observe(name="chat_query")
def chat(request: ChatRequest, background_tasks: BackgroundTasks) -> ChatResponse:
    # sets what shows as this trace's input in the dashboard
    get_client().update_current_span(input={"question": request.question})

    # Step 1: convert the question into a vector, same way chunks were embedded.
    query_vector = embed_text(request.question)

    # Step 2: find the most relevant chunks stored in Qdrant.
    matches = search(query_vector, limit=3)

    # Step 3: combine the matched chunks' text into one context block for the LLM.
    context_texts = [match["text"] for match in matches]
    context = "\n\n".join(context_texts)

    # Step 4: ask the local LLM to answer, grounded in that context.
    answer = generate_answer(request.question, context)
    # sets what shows as this trace's output in the dashboard
    get_client().update_current_span(output={"answer": answer})

    # captures the trace ID now, while it's still active
    trace_id = get_client().get_current_trace_id()
    # schedules scoring to run after the response is sent, not blocking the user
    background_tasks.add_task(_score_and_log, trace_id, request.question, context_texts, answer)

    # sends the answer back to the client
    return ChatResponse(answer=answer)
