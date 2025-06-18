from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Session:
    """Represents a user session."""
    def __init__(self, session_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.session_id = session_id
        self.metadata = metadata if metadata is not None else {}
        # You can add other common session attributes here, e.g., creation_time, last_accessed_time

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Gets a value from session metadata."""
        return self.metadata.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets a value in session metadata."""
        self.metadata[key] = value

    def __str__(self) -> str:
        return f"Session(session_id='{self.session_id}', metadata={self.metadata})"

class BaseSessionService(ABC):
    """Abstract base class for session management services."""

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieves a session by its ID."""
        pass

    @abstractmethod
    def create_session(self, session_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Session:
        """Creates a new session, generating an ID if not provided."""
        pass

    @abstractmethod
    def save_session(self, session: Session) -> None:
        """Saves (updates) a session."""
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        """Deletes a session by its ID."""
        pass