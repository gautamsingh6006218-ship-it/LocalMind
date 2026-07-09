from app.ingestion.ingest import chunk_text


def test_chunk_text_splits_into_expected_sizes():
    # 25 characters, chunk_size=10 -> should produce 3 chunks: 10, 10, 5
    text = "a" * 25
    chunks = chunk_text(text, chunk_size=10)

    assert len(chunks) == 3
    assert len(chunks[0]) == 10
    assert len(chunks[1]) == 10
    assert len(chunks[2]) == 5


def test_chunk_text_preserves_all_content():
    # Joining the chunks back together should reproduce the original text exactly -
    # confirms no characters are lost or duplicated during slicing.
    text = "The quick brown fox jumps over the lazy dog."
    chunks = chunk_text(text, chunk_size=7)

    assert "".join(chunks) == text


def test_chunk_text_empty_string_returns_no_chunks():
    assert chunk_text("", chunk_size=10) == []


def test_chunk_text_shorter_than_chunk_size_returns_one_chunk():
    text = "short"
    chunks = chunk_text(text, chunk_size=500)

    assert chunks == ["short"]
