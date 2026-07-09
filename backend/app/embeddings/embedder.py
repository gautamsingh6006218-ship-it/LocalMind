from sentence_transformers import SentenceTransformer
from langfuse import observe

from app.config import EMBEDDING_MODEL

# Loaded once when this module is first imported, not on every call -
# loading the model is slow, so we don't want to repeat it per request.
_model = SentenceTransformer(EMBEDDING_MODEL)


@observe()
def embed_text(text: str) -> list[float]:
    """Embeds the given text into a vector using the configured embedding model."""
    # .tolist() converts the NumPy array output into a plain Python list, since
    # that's the format needed to serialize this vector into a JSON request later.
    return _model.encode(text).tolist()
