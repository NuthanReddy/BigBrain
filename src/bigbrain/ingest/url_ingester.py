"""URL/web page ingester — fetches and extracts text from web pages."""

from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import urlparse

import html2text
import httpx
from bs4 import BeautifulSoup

from bigbrain.errors import FileAccessError
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class UrlIngester:
    """Ingests web pages by fetching HTML and extracting text."""

    def __init__(self, *, timeout: int = 30, max_size_mb: int = 10) -> None:
        self._timeout = timeout
        self._max_size = max_size_mb * 1024 * 1024

    def ingest(self, url: str) -> Document:
        """Fetch a URL and return a Document with extracted text.

        Args:
            url: The web page URL to fetch

        Returns:
            Document with title, content (plain text), and sections (by headings)

        Raises:
            FileAccessError: On fetch failures, timeouts, or invalid responses
        """
        html = self._fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        title = self._extract_title(soup, url)

        # Remove non-content elements before text conversion
        for tag in soup.find_all(
            ["script", "style", "nav", "footer", "header", "aside"]
        ):
            tag.decompose()

        sections = self._extract_sections(soup)

        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True
        converter.body_width = 0  # No wrapping
        plain_text = converter.handle(str(soup)).strip()

        source = SourceMetadata(
            file_path=url,
            file_extension=".html",
            source_type="url",
            modified_at=datetime.now(timezone.utc),
            size_bytes=len(plain_text.encode("utf-8")),
            extra={
                "url": url,
                "content_type": self._last_content_type,
                "final_url": self._last_final_url,
                "status_code": self._last_status_code,
            },
        )

        return Document(
            title=title,
            content=plain_text,
            source=source,
            language="",
            sections=sections,
            metadata={"url": url, "fetched_at": datetime.now(timezone.utc).isoformat()},
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fetch(self, url: str) -> str:
        """Fetch the raw HTML for *url*, raising FileAccessError on failure."""
        try:
            resp = httpx.get(
                url,
                follow_redirects=True,
                timeout=self._timeout,
                headers={"User-Agent": "BigBrain/1.0 (Knowledge Compiler)"},
            )
            resp.raise_for_status()
        except httpx.TimeoutException:
            raise FileAccessError(url, f"Request timed out after {self._timeout}s")
        except httpx.HTTPStatusError as exc:
            raise FileAccessError(url, f"HTTP {exc.response.status_code}")
        except httpx.ConnectError:
            raise FileAccessError(url, "Cannot connect")
        except Exception as exc:
            raise FileAccessError(url, str(exc))

        content_type = resp.headers.get("content-type", "")
        if "html" not in content_type and "text" not in content_type:
            raise FileAccessError(url, f"Unsupported content type: {content_type}")

        if len(resp.content) > self._max_size:
            raise FileAccessError(
                url, f"Response too large: {len(resp.content)} bytes"
            )

        # Stash response metadata for SourceMetadata
        self._last_content_type = content_type
        self._last_final_url = str(resp.url)
        self._last_status_code = resp.status_code

        return resp.text

    @staticmethod
    def _extract_title(soup: BeautifulSoup, url: str) -> str:
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if title:
                return title
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
            if title:
                return title
        parsed = urlparse(url)
        return parsed.netloc + parsed.path

    @staticmethod
    def _extract_sections(soup: BeautifulSoup) -> list[DocumentSection]:
        """Extract sections based on heading tags."""
        sections: list[DocumentSection] = []
        heading_tags = ["h1", "h2", "h3", "h4"]

        for tag in soup.find_all(heading_tags):
            heading_text = tag.get_text(strip=True)
            if not heading_text:
                continue

            content_parts: list[str] = []
            for sibling in tag.next_siblings:
                if sibling.name in heading_tags:
                    break
                text = (
                    sibling.get_text(strip=True)
                    if hasattr(sibling, "get_text")
                    else str(sibling).strip()
                )
                if text:
                    content_parts.append(text)

            level = int(tag.name[1])
            sections.append(
                DocumentSection(
                    title=heading_text,
                    content="\n".join(content_parts),
                    level=level,
                )
            )

        return sections
