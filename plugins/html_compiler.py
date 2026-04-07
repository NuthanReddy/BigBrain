"""Example plugin: HTML output compiler."""

from bigbrain.compile.models import CompileOutput, OutputFormat
from bigbrain.kb.models import Document
from bigbrain.plugins.base import CompilePlugin, PluginInfo


class HtmlCompilerPlugin(CompilePlugin):
    """Compiles distilled content into an HTML page."""

    def info(self) -> PluginInfo:
        return PluginInfo(
            name="html_compiler",
            version="1.0.0",
            description="Export knowledge as standalone HTML pages",
            author="BigBrain",
            plugin_type="compiler",
        )

    def format_name(self) -> str:
        return "html"

    def compile(self, doc, summaries, entities, relationships) -> CompileOutput:
        parts = [
            "<!DOCTYPE html>",
            "<html><head>",
            f"<title>{doc.title}</title>",
            "<style>body{font-family:sans-serif;max-width:800px;margin:0 auto;padding:20px}</style>",
            "</head><body>",
            f"<h1>{doc.title}</h1>",
        ]

        if summaries:
            parts.append("<h2>Summary</h2>")
            for s in summaries:
                parts.append(f"<p>{s.content}</p>")

        if entities:
            parts.append("<h2>Key Concepts</h2><ul>")
            for e in entities:
                desc = f" — {e.description}" if e.description else ""
                parts.append(
                    f"<li><strong>{e.name}</strong> ({e.entity_type}){desc}</li>"
                )
            parts.append("</ul>")

        parts.append("</body></html>")

        return CompileOutput(
            format=OutputFormat.MARKDOWN,  # reuse existing enum
            title=f"{doc.title} — HTML",
            content="\n".join(parts),
            source_doc_id=doc.id,
            source_doc_title=doc.title,
        )
