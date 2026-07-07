from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

COLLECTION_NAME = "localmind"

# Must be the exact same model used during ingestion - a query embedded with a
# different model would land in a different vector space, making the similarity
# search meaningless (comparing apples to oranges).
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

question = "What is the meaning of life?"

# .tolist() converts the NumPy array output into a plain Python list, since that's
# the format the Qdrant client needs to serialize this vector into a JSON request.
query_vector = model.encode(question).tolist()

# Connects to the same Qdrant container ingest.py wrote data into.
client = QdrantClient("http://localhost:6333")

# Sends query_vector to Qdrant, which compares it against all stored vectors using
# Cosine similarity (as configured when the collection was created) and returns
# the `limit` closest matches - the chunks most relevant to the question.
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=3,
)

# Each `point` here is a match: .score = how similar (closer to 1 = more similar),
# .payload = the original chunk text + source filename we stored during ingestion.
for point in results.points:
    print(f"Score: {point.score}, Text: {point.payload['text']}, Source: {point.payload['source']}")
