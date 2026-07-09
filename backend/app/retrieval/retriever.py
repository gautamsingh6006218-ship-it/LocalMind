from qdrant_client import QdrantClient
from langfuse import observe

from app.config import QDRANT_URL, QDRANT_COLLECTION

# Connects once at import time, reused across calls - same reasoning as the
# embedding model: setting up a fresh connection on every request is wasteful.
_client = QdrantClient(QDRANT_URL)


@observe()
def search(query_vector: list[float], limit: int = 3) -> list[dict]:
    """Find the `limit` chunks most similar to query_vector."""
    # Sends query_vector to Qdrant, which compares it against all stored vectors
    # using Cosine similarity (as configured when the collection was created).
    results = _client.query_points(
        collection_name=QDRANT_COLLECTION,
        query=query_vector,
        limit=limit,
    )

    # Flatten each match into a plain dict - callers don't need to know about
    # Qdrant's internal ScoredPoint structure, just score/text/source.
    return [
        {
            "score": point.score,
            "text": point.payload["text"],
            "source": point.payload["source"],
        }
        for point in results.points
    ]
