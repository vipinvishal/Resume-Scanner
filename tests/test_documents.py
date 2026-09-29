import io, zipfile
import pytest
from docx import Document
from app.adapters.documents import DocumentError, parse_docx, parse_pdf
def docx_bytes(text="Experience\n"+"Built reliable cloud systems. "*15):
    d=Document(); d.add_paragraph(text); out=io.BytesIO(); d.save(out); return out.getvalue()
def test_digital_docx_passes(): assert parse_docx(docx_bytes()).segments
def test_malformed_docx_fails():
    with pytest.raises(DocumentError): parse_docx(b"not a docx")
def test_oversize_fails():
    with pytest.raises(DocumentError): parse_docx(b"x"*(5_242_881))
def test_archive_expansion_abuse_fails(monkeypatch):
    data=docx_bytes(); real=zipfile.ZipFile.infolist
    class I: file_size=25_000_001
    monkeypatch.setattr(zipfile.ZipFile,"infolist",lambda self:[I()])
    with pytest.raises(DocumentError): parse_docx(data)
def test_invalid_pdf_signature_fails():
    with pytest.raises(DocumentError): parse_pdf(b"not pdf")
