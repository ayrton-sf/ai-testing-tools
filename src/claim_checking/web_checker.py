from typing import Dict, List, Union
import io
from PyPDF2 import PdfReader
from src.claim_checking.claim_checker import ClaimChecker
import requests
import re
from bs4 import BeautifulSoup
from src.llm.llm_service import LLMService


class WebChecker(ClaimChecker):
    def __init__(self, llm_service: LLMService):
        self.MAX_CHUNK_CHARS = 4000
        self.llm_service = llm_service

    def fetch_reference(self, urls: List[str]) -> List[str]:
        texts = []
        for url in urls:
            response = requests.get(url)
            content_type = response.headers.get("Content-Type", "")

            if url.lower().endswith(".pdf") or "application/pdf" in content_type:
                pdf_bytes = response.content
                texts.append(self._extract_text_from_pdf(pdf_bytes))
            else:
                html_str = response.text
                texts.append(self._extract_text_from_html(html_str))

        return texts

    def chunk_content(self, content: List[str]) -> List[str]:
        all_chunks = []
        for piece in content:
            parts = [s.strip() for s in re.split(r"\.\n", piece) if s.strip()]
            all_chunks.extend(parts)

        grouped = []
        current = ""
        length = 0

        for chunk in all_chunks:
            if len(chunk) > self.MAX_CHUNK_CHARS:
                for i in range(0, len(chunk), self.MAX_CHUNK_CHARS):
                    part = chunk[i : i + self.MAX_CHUNK_CHARS]
                    if length + len(part) > self.MAX_CHUNK_CHARS:
                        if current:
                            grouped.append(current)
                        current = part
                        length = len(part)
                    else:
                        current += part
                        length += len(part)
                continue

            if length + len(chunk) > self.MAX_CHUNK_CHARS:
                grouped.append(current)
                current = chunk
                length = len(chunk)
            else:
                current += chunk
                length += len(chunk)

        if current:
            grouped.append(current)

        return grouped

    def _extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text_chunks = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

        return "\n".join(text_chunks)

    def _extract_text_from_html(self, html_str: str) -> str:
        soup = BeautifulSoup(html_str, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = (line.strip() for line in text.splitlines())
        chunks = [line for line in lines if line]

        return "\n".join(chunks)
