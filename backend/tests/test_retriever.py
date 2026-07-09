from app.embeddings.embedder import embed_text
from app.retrieval.retriever import search


def test_search_returns_requested_number_of_results():
    query_vector = embed_text("What is the meaning of life?")
    results = search(query_vector, limit=3)

    assert len(results) == 3


def test_search_results_have_expected_shape():
    query_vector = embed_text("What is the meaning of life?")
    results = search(query_vector, limit=3)

    for result in results:
        assert "score" in result
        assert "text" in result
        assert "source" in result
        assert isinstance(result["text"], str)


def test_search_results_are_sorted_by_descending_score():
    # Qdrant should always return the closest matches first - verifies
    # we're not accidentally getting results in an arbitrary order.
    query_vector = embed_text("What is the meaning of life?")
    results = search(query_vector, limit=3)

    scores = [result["score"] for result in results]
    assert scores == sorted(scores, reverse=True)


def test_relevant_query_scores_higher_than_irrelevant_query():
    # sample.txt discusses wealth/inequality topics (confirmed via manual testing
    # earlier) - a query about that topic should score higher than a query about
    # something the document doesn't cover at all, proving search actually
    # discriminates between relevant and irrelevant content.
    relevant_vector = embed_text("How should wealth be distributed fairly?")
    irrelevant_vector = embed_text("What is the boiling point of nitrogen?")

    relevant_top_score = search(relevant_vector, limit=1)[0]["score"]
    irrelevant_top_score = search(irrelevant_vector, limit=1)[0]["score"]

    assert relevant_top_score > irrelevant_top_score
