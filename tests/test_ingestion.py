from pathlib import Path

import pytest
from langchain_core.documents import Document

from app.services.ingestion import SUPPORTED, chunk_documents, load_file


def test_supported_extensions():
    assert {".pdf", ".txt", ".md", ".docx"} <= SUPPORTED


def test_load_markdown_file(tmp_path: Path):
    f = tmp_path / "vpn.md"
    f.write_text("# VPN\nReset your VPN password from the self-service portal.", encoding="utf-8")
    docs = load_file(f)
    assert len(docs) == 1
    assert "VPN" in docs[0].page_content


def test_load_unsupported_file_raises(tmp_path: Path):
    f = tmp_path / "image.png"
    f.write_bytes(b"not really an image")
    with pytest.raises(ValueError):
        load_file(f)


def test_chunking_splits_long_text():
    text = "Printer troubleshooting steps. " * 200
    chunks = chunk_documents([Document(page_content=text, metadata={"source": "x"})])
    assert len(chunks) > 1
    assert all(c.page_content.strip() for c in chunks)
    assert all("start_index" in c.metadata for c in chunks)