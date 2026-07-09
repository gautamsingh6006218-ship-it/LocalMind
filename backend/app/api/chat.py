from fastapi import APIRouter
from pydantic import BaseModel
from langfuse import observe, get_client
from app.embeddings.embedder import embed_text
from app.llm.ollama_client import generate_answer
from app.retrieval.retriever import search

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post("/chat")
@observe(name="chat_query")
def chat(request: ChatRequest) -> ChatResponse:

    get_client().update_current_span(input={"question": request.question})
    # Step 1: convert the question into a vector, same way chunks were embedded.
    query_vector = embed_text(request.question)

    # Step 2: find the most relevant chunks stored in Qdrant.
    matches = search(query_vector, limit=3)

    # Step 3: combine the matched chunks' text into one context block for the LLM.
    context = "\n\n".join(match["text"] for match in matches)

    # Step 4: ask the local LLM to answer, grounded in that context.
    answer = generate_answer(request.question, context)

    get_client().update_current_span(output={"answer": answer})

    return ChatResponse(answer=answer)
