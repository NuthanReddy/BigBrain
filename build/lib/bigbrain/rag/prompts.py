"""Prompt templates for RAG operations."""

from __future__ import annotations

# QA prompt — answer a question given context
QA_SYSTEM = (
    "You are a knowledgeable assistant. Answer questions accurately based on "
    "the provided context. Be clear and concise. If the context doesn't contain "
    "enough information to answer fully, say so and share what you can."
)

QA_TEMPLATE = (
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

# Summarize prompt — summarize a document/section
SUMMARIZE_TEMPLATE = (
    "Summarize the following text concisely. Focus on key concepts, "
    "definitions, algorithms, and important details.\n\n"
    "Text:\n{text}\n\n"
    "Summary:"
)

# Explain prompt — explain a concept
EXPLAIN_TEMPLATE = (
    "Context:\n{context}\n\n"
    "Explain the following concept clearly, using examples from the context "
    "where relevant:\n\n"
    "Concept: {question}\n\n"
    "Explanation:"
)


def build_qa_messages(question: str, context: str) -> list[dict[str, str]]:
    """Build chat messages for a QA query."""
    return [
        {"role": "system", "content": QA_SYSTEM},
        {"role": "user", "content": QA_TEMPLATE.format(context=context, question=question)},
    ]


def build_qa_prompt(question: str, context: str) -> str:
    """Build a single completion prompt for QA."""
    return f"{QA_SYSTEM}\n\n{QA_TEMPLATE.format(context=context, question=question)}"


def build_summarize_prompt(text: str) -> str:
    """Build a summarization prompt."""
    return SUMMARIZE_TEMPLATE.format(text=text)


def build_explain_messages(question: str, context: str) -> list[dict[str, str]]:
    """Build chat messages for an explain query."""
    return [
        {"role": "system", "content": QA_SYSTEM},
        {"role": "user", "content": EXPLAIN_TEMPLATE.format(context=context, question=question)},
    ]
