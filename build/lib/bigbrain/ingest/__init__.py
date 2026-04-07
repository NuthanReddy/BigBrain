"""Ingest – read source material into a common Document model."""

from bigbrain.ingest.registry import BaseIngester, get_ingester, register_ingester
from bigbrain.ingest.service import ingest_path

__all__ = ["BaseIngester", "get_ingester", "register_ingester", "ingest_path"]
