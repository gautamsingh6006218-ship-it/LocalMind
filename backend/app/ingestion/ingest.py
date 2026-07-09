from pathlib import Path

from app.embeddings.embedder import embed_texts
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config import QDRANT_URL, QDRANT_COLLECTION

chunk_size = 500


def chunk_text(text: str, chunk_size: int = chunk_size):
    """Chunk the text into smaller pieces."""
    # Naive fixed-size chunking: slice the string every `chunk_size` characters.
    # Doesn't respect sentence/paragraph boundaries yet - good enough to prove the pipeline works.
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def main():
    file_path = Path("data/sample.txt")
    text = file_path.read_text()
    chunks = chunk_text(text)

    # Loads the configured embedding model (downloads it on first run) and converts
    # each chunk of text into a vector.

    embeddings = embed_texts(chunks)

    # Connects to the Qdrant container we started via docker-compose.
    client = QdrantClient(QDRANT_URL)

    # Only create the collection (Qdrant's version of a "table") if it doesn't exist yet -
    # otherwise re-running this script would error trying to recreate it.
    if not client.collection_exists(QDRANT_COLLECTION):
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            # size must match the embedding model's output dimension (1024 here)
            vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE),
        )

    # Build one "point" per chunk: its vector (for similarity search) plus a payload
    # (the original text + source filename) so we can retrieve human-readable results later.
    points = [
        PointStruct(id=i, vector=embeddings[i], payload={"text": chunks[i], "source": file_path.name})
        for i in range(len(chunks))
    ]

    # Writes (or overwrites, since IDs are reused on rerun) all points into Qdrant in one call.
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"Inserted {len(chunks)} chunks from {file_path.name}")


if __name__ == "__main__":
    main()
