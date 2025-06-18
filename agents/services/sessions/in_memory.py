import uuid
from typing import Dict, Optional, Any

from .base import BaseSessionService, Session

class InMemorySessionService(BaseSessionService):
    """An in-memory session service implementation."""

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def create_session(self, session_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Session:
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id in self._sessions:
            # Or raise an error, or return existing session, depending on desired behavior
            return self._sessions[session_id] 
            
        session = Session(session_id, metadata)
        self._sessions[session_id] = session
        return session

    def save_session(self, session: Session) -> None:
        # In-memory save is implicit when attributes of the session object are modified,
        # but this method is here to conform to the interface and for potential future logic.
        if session.session_id not in self._sessions:
            # Optionally, handle cases where a session is saved without being formally created
            # For now, we'll just add it.
            self._sessions[session.session_id] = session
        # If it exists, it's already the same object in memory, so changes are reflected.
        return

    def delete_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]