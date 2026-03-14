"""Memory management systems for agentic workflows.

This module provides two tiers of memory to support conversational agents:
1. `ShortTermMemory`: A session-based, in-memory store for tracking the
    immediate history of execution (Runs, States, etc.) within a local context.
2. `LongTermMemory`: A persistent, vector-backed store for user preferences
    and facts that should survive across multiple sessions or deployments.

Design notes:
- Short-term memory uses deep copies to prevent side effects between steps.
- Long-term memory uses semantic search (vector embeddings) for retrieval.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import copy

from lib.documents import Document, Corpus
from lib.vector_db import VectorStoreManager,QueryResult


class SessionNotFoundError(Exception):
    """Raised when attempting to access a session that doesn't exist"""
    pass


@dataclass
class ShortTermMemory():
    """Manages the history of objects across multiple conversation sessions.

    `ShortTermMemory` acts as the "working memory" for the agent system. It
    organizes execution data (like `Run` objects from a state machine) into
    isolated sessions. Each session maintains a chronological list of events.

    Key behaviors:
    - Deep-copies objects when adding to history to ensure data immutability.
    - Automatically initializes a "default" session if none is specified.
    - Provides lifecycle management (create, reset, delete) for sessions.

    Attributes:
        sessions (Dict[str, List[Any]]): A mapping of session IDs to their
            respective chronological object lists.
    """
    sessions: Dict[str, List[Any]] = field(default_factory=lambda: {})

    def __post_init__(self):
        """Initialize the default session upon creation."""
        self.create_session("default")

    def __str__(self) -> str:
        session_ids = list(self.sessions.keys())
        return f"Memory(sessions={session_ids})"

    def __repr__(self) -> str:
        return self.__str__()

    def create_session(self, session_id: str) -> bool:
        """Initialize a new isolated memory session.
        
        Args:
            session_id: A unique identifier for the session (e.g., a user ID
                or a specific conversation UUID).
            
        Returns:
            bool: True if the session was newly created, False if it already
                existed (preserving the existing history).
        """
        if session_id in self.sessions:
            return False
        self.sessions[session_id] = []
        return True

    def delete_session(self, session_id: str) -> bool:
        """Permanently remove a session and all its stored history.
        
        Args:
            session_id: Identifier of the session to delete.
            
        Returns:
            bool: True if the session was found and deleted, False otherwise.
            
        Raises:
            ValueError: If attempting to delete the 'default' session, which
                must always exist for system stability.
        """
        if session_id == "default":
            raise ValueError("Cannot delete the default session")
        if session_id not in self.sessions:
            return False
        del self.sessions[session_id]
        return True

    def _validate_session(self, session_id: str):
        """Internal helper to verify session existence.
        
        Args:
            session_id: The ID to check against active sessions.
            
        Raises:
            SessionNotFoundError: If the ID does not map to an existing session.
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session '{session_id}' not found")

    def add(self, object: Any, session_id: Optional[str] = None):
        """Append a new object to a session's history.
        
        The object is deep-copied before being stored to prevent future
        modifications to the in-memory history from affecting external state.
        
        Args:
            object: The data or object to store (e.g., a `Run` result).
            session_id: The session ID to append to. Defaults to "default".
            
        Raises:
            SessionNotFoundError: If the specified session has not been created.
        """
        session_id = session_id or "default"
        self._validate_session(session_id)
        self.sessions[session_id].append(copy.deepcopy(object))

    def get_all_objects(self, session_id: Optional[str] = None) -> List[Any]:
        """Retrieve the complete chronological history of a session.
        
        Args:
            session_id: The target session ID. Defaults to "default".
            
        Returns:
            List[Any]: A list of deep-copied objects from the history.
            
        Raises:
            SessionNotFoundError: If the session doesn't exist.
        """
        session_id = session_id or "default"
        self._validate_session(session_id)
        return [copy.deepcopy(obj) for obj in self.sessions[session_id]]

    def get_last_object(self, session_id: Optional[str] = None) -> Optional[Any]:
        """Retrieve the most recently added object from a session.
        
        Args:
            session_id: The target session ID. Defaults to "default".
            
        Returns:
            Optional[Any]: The last object in the list, or None if the
                session history is currently empty.
            
        Raises:
            SessionNotFoundError: If the session doesn't exist.
        """
        objects = self.get_all_objects(session_id)
        return objects[-1] if objects else None

    def get_all_sessions(self) -> List[str]:
        """Return a list of all currently active session IDs."""
        return list(self.sessions.keys())

    def reset(self, session_id: Optional[str] = None):
        """Clear the history of a specific session or all sessions.
        
        Args:
            session_id: Identifier of the session to clear. If None,
                every active session is wiped clean.
            
        Raises:
            SessionNotFoundError: If a specific session_id is provided
                but does not exist.
        """
        if session_id is None:
            # Reset all sessions to empty lists
            for sid in self.sessions:
                self.sessions[sid] = []
        else:
            self._validate_session(session_id)
            self.sessions[session_id] = []

    def pop(self, session_id: Optional[str] = None) -> Optional[Any]:
        """Remove and return the most recent object from a session.
        
        Args:
            session_id: The target session ID. Defaults to "default".
            
        Returns:
            Optional[Any]: The removed object, or None if empty.
            
        Raises:
            SessionNotFoundError: If the session doesn't exist.
        """
        session_id = session_id or "default"
        self._validate_session(session_id)
        
        if not self.sessions[session_id]:
            return None
        return self.sessions[session_id].pop()

@dataclass
class MemoryFragment:
    """
    Represents a single piece of memory information stored in the long-term memory system.
    
    This class encapsulates user preferences, facts, or contextual information that can be
    retrieved later to provide personalized responses in conversational AI applications.
    
    Attributes:
        content (str): The actual memory content or information to be stored
        owner (str): Identifier for the user who owns this memory fragment
        namespace (str): Logical grouping for organizing related memories (default: "default")
        timestamp (int): Unix timestamp when the memory was created (auto-generated)
    """
    content: str
    owner: str 
    namespace: str = "default"
    timestamp: int = field(default_factory=lambda: int(datetime.now().timestamp()))


@dataclass
class MemorySearchResult:
    """
    Container for the results of a memory search operation.
    
    Encapsulates both the retrieved memory fragments and associated metadata
    such as distance scores from the vector search.
    
    Attributes:
        fragments (List[MemoryFragment]): List of memory fragments matching the search query
        metadata (Dict): Additional information about the search results (e.g., distances, scores)
    """
    fragments: List[MemoryFragment]
    metadata: Dict

@dataclass
class TimestampFilter:
    """
    Filter criteria for time-based memory searches.
    
    Allows filtering memory fragments based on when they were created,
    enabling retrieval of recent memories or memories from specific time periods.
    
    Attributes:
        greater_than_value (int, optional): Unix timestamp - only return memories created after this time
        lower_than_value (int, optional): Unix timestamp - only return memories created before this time
    """
    greater_than_value: int = None
    lower_than_value: int = None

class LongTermMemory:
    """
    Manages persistent memory storage and retrieval using vector embeddings.
    
    This class provides a high-level interface for storing and searching user memories,
    preferences, and contextual information across conversation sessions. It uses
    vector similarity search to find relevant memories based on semantic meaning.
    
    The memory system supports:
    - Multi-user memory isolation
    - Namespace-based organization
    - Time-based filtering
    - Semantic similarity search
    """
    def __init__(self, db:VectorStoreManager):
        self.vector_store = db.create_store("long_term_memory", force=True)

    def get_namespaces(self) -> List[str]:
        """
        Retrieve all unique namespaces currently stored in memory.
        
        Useful for understanding how memories are organized and for
        administrative purposes.
        
        Returns:
            List[str]: List of unique namespace identifiers
        """
        results = self.vector_store.get()
        namespaces = [r["metadatas"][0]["namespace"] for r in results]
        return namespaces

    def register(self, memory_fragment:MemoryFragment, metadata:Optional[Dict[str, str]]=None):
        """
        Store a new memory fragment in the long-term memory system.
        
        The memory is converted to a vector embedding and stored with associated
        metadata for later retrieval. Additional metadata can be provided to
        enhance searchability.
        
        Args:
            memory_fragment (MemoryFragment): The memory content to store
            metadata (Optional[Dict[str, str]]): Additional metadata to associate with the memory
        """
        complete_metadata = {
            "owner": memory_fragment.owner,
            "namespace": memory_fragment.namespace,
            "timestamp": memory_fragment.timestamp,
        }
        if metadata:
            complete_metadata.update(metadata)

        self.vector_store.add(
            Document(
                content=memory_fragment.content,
                metadata=complete_metadata,
            )
        )

    def search(self, query_text:str, owner:str, limit:int=3,
               timestamp_filter:Optional[TimestampFilter]=None, 
               namespace:Optional[str]="default") -> MemorySearchResult:
        """
        Search for relevant memories using semantic similarity.
        
        Performs a vector similarity search to find memories that are semantically
        related to the query text. Results are filtered by owner, namespace, and
        optionally by timestamp range.
        
        Args:
            query_text (str): The search query to find similar memories
            owner (str): User identifier to filter memories by ownership
            limit (int): Maximum number of results to return (default: 3)
            timestamp_filter (Optional[TimestampFilter]): Time-based filtering criteria
            namespace (Optional[str]): Namespace to search within (default: "default")
            
        Returns:
            MemorySearchResult: Container with matching memory fragments and metadata
        """

        where = {
            "$and": [
                {
                    "namespace": {
                        "$eq": namespace
                    }
                },
                {
                    "owner": {
                        "$eq": owner
                    }
                },
            ]
        }

        if timestamp_filter:
            if timestamp_filter.greater_than_value:
                where["$and"].append({
                    "timestamp": {
                        "$gt": timestamp_filter.greater_than_value,
                    }
                })
            if timestamp_filter.lower_than_value:
                where["$and"].append({
                    "timestamp": {
                        "$lt": timestamp_filter.lower_than_value,
                    }
                })

        result:QueryResult = self.vector_store.query(
            query_texts=[query_text],
            n_results=limit,
            where=where
        )

        fragments = []
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        for content, meta in zip(documents, metadatas):
            owner = meta.get("owner")
            namespace = meta.get("namespace", "default")
            timestamp = meta.get("timestamp")

            fragment = MemoryFragment(
                content=content,
                owner=owner,
                namespace=namespace,
                timestamp=timestamp
            )

            fragments.append(fragment)
        
        result_metadata = {
            "distances": result.get("distances", [[]])[0]
        }

        return MemorySearchResult(
            fragments=fragments,
            metadata=result_metadata
        )
