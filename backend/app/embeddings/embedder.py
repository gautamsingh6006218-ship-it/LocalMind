from sentence_transformers import SentenceTransformer
from langfuse import observe

# Loaded once when this module is first imported, not on every call -
# loading the model is slow, so we don't want to repeat it per request.
_model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

@observe()
def embed_text(text: str) -> list[float]:
    """Embeds the given text into a vector using the Qwen3-Embedding-0.6B model into 1024 dimensions."""
    # .tolist() converts the NumPy array output into a plain Python list, since
    # that's the format needed to serialize this vector into a JSON request later.
    return _model.encode(text).tolist()
