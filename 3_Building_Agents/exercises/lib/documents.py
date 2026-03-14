"""Document and Corpus abstractions for RAG and agent applications.

This module provides the core data structures used to represent information
within the agentic system. It defines `Document` as the atomic unit of text
and `Corpus` as a managed collection of documents with batch processing
capabilities.

Key concepts:
- `Document`: A single chunk of text with a unique ID and optional metadata.
- `Corpus`: A list-like container that ensures type safety and provides
    helpers for vector database integration.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import uuid
from collections.abc import MutableSequence


@dataclass
class Document:
    """The atomic unit of information in the system.

    A `Document` wraps a piece of text (content) with a unique identifier
    and a flexible metadata dictionary. This structure is the primary
    format for indexing in vector databases and retrieved context in RAG.

    Attributes:
        id (str): A unique identifier (auto-generated as UUID if not provided).
        content (str): The actual text content to be processed or searched.
        metadata (Dict[str, Any]): Optional key-value pairs (e.g., source,
            page number, author) used for filtering during retrieval.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = field(default_factory=str)
    metadata: Dict[str, Any] = None


class Corpus(MutableSequence):
    """A type-safe collection of Document objects.

    `Corpus` behaves like a Python list but enforces that only `Document`
    instances can be added. It also provides utility methods to convert
    the entire collection into formats required by batch processing systems
    like ChromaDB or OpenAI's batch API.

    Usage:
        corpus = Corpus()
        corpus.append(Document(content="Hello world"))
        data = corpus.to_dict()  # Ready for vector DB ingestion
    """

    def __init__(self, documents: Optional[List[Document]] = None):
        """Initialize a new Corpus.

        Args:
            documents: An optional initial list of Document objects.
        """
        self._documents = documents or []

    def __getitem__(self, index):
        """Retrieve a document by its index."""
        return self._documents[index]

    def __setitem__(self, index, value: Document):
        """Set a document at a specific index, enforcing Document type."""
        if not isinstance(value, Document):
            raise TypeError("Collection only supports Document items")
        self._documents[index] = value

    def __delitem__(self, index):
        """Delete a document from the collection by index."""
        del self._documents[index]

    def __len__(self):
        """Return the total number of documents in the corpus."""
        return len(self._documents)

    def insert(self, index, value: Document):
        """Insert a document at a specific position, enforcing Document type."""
        if not isinstance(value, Document):
            raise TypeError("Collection only supports Document items")
        self._documents.insert(index, value)

    def to_dict(self) -> Dict[str, List[Any]]:
        """
        Convert the corpus to a dictionary format suitable for batch operations.

        This method extracts all document contents, metadata, and IDs into
        separate lists, which is the format typically expected by vector
        databases and other batch processing systems. This allows for efficient
        bulk operations on the entire corpus.

        Returns:
            Dict[str, List[Any]]: Dictionary containing:
                - 'contents': List of all document content strings
                - 'metadatas': List of all document metadata dictionaries
                - 'ids': List of all document ID strings

        Example:
            >>> corpus = Corpus([doc1, doc2])
            >>> batch_data = corpus.to_dict()
            >>> chroma_collection.add(
            ...     documents=batch_data['contents'],
            ...     metadatas=batch_data['metadatas'],
            ...     ids=batch_data['ids']
            ... )
        """

        # Use zip with unpacking to efficiently extract all fields
        # Handle empty corpus case by providing empty defaults
        contents, metadatas, ids = zip(*(
            (doc.content, doc.metadata, doc.id) for doc in self._documents
        )) if self._documents else ([], [], [])

        return {
            'contents': list(contents),
            'metadatas': list(metadatas),
            'ids': list(ids)
        }
