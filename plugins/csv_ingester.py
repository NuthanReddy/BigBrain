"""Example plugin: CSV file ingester."""

import csv
from pathlib import Path

from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.plugins.base import IngestPlugin, PluginInfo


class CsvIngesterPlugin(IngestPlugin):
    """Ingests CSV files into the knowledge base."""

    def info(self) -> PluginInfo:
        return PluginInfo(
            name="csv_ingester",
            version="1.0.0",
            description="Ingest CSV files as structured documents",
            author="BigBrain",
            plugin_type="ingester",
        )

    def supported_extensions(self) -> list[str]:
        return [".csv"]

    def ingest(self, path: Path) -> Document:
        path = Path(path)
        rows: list[dict[str, str]] = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            for row in reader:
                rows.append(row)

        # Build text content
        lines = [", ".join(headers)]
        for row in rows:
            lines.append(", ".join(str(v) for v in row.values()))
        content = "\n".join(lines)

        stat = path.stat()
        return Document(
            title=path.stem.replace("_", " ").title(),
            content=content,
            source=SourceMetadata(
                file_path=str(path),
                file_extension=".csv",
                source_type="csv",
                size_bytes=stat.st_size,
            ),
            sections=[
                DocumentSection(
                    title="Data",
                    content=content,
                    level=1,
                    metadata={
                        "rows": len(rows),
                        "columns": len(headers),
                        "headers": headers,
                    },
                )
            ],
            metadata={"row_count": len(rows), "column_count": len(headers)},
        )
