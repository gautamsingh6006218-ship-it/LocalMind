from app.embeddings.embedder import embed_text


def test_embed_text_returns_correct_dimension():
    # Qwen3-Embedding-0.6B always outputs 1024 numbers per text, regardless of
    # how long or short the input is - this is a property of the model itself.
    vector = embed_text("hello world")

    assert len(vector) == 1024


def test_embed_text_returns_plain_list_of_floats():
    # Must be a plain Python list (not a NumPy array) so it can be sent to
    # Qdrant as JSON - this is what the .tolist() conversion is for.
    vector = embed_text("hello world")

    assert isinstance(vector, list)
    assert all(isinstance(x, float) for x in vector)


def test_similar_sentences_produce_closer_vectors_than_unrelated_ones():
    # We can't assert exact output values (that's an internal detail of the
    # model), but we CAN assert the model behaves sensibly: two sentences about
    # the same topic should be more similar to each other than to an unrelated one.
    import numpy as np

    cooking_1 = embed_text("I love cooking pasta with tomato sauce.")
    cooking_2 = embed_text("Pasta with tomato sauce is my favorite dish.")
    unrelated = embed_text("The stock market crashed yesterday.")

    def cosine_similarity(a, b):
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    sim_related = cosine_similarity(cooking_1, cooking_2)
    sim_unrelated = cosine_similarity(cooking_1, unrelated)

    assert sim_related > sim_unrelated
