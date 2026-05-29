
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

class Message:
    """Modela um objeto de mensagem mínimo."""
    author_id: str # User ID (Author ID)
    author_name: str # User Name (Author Name)
    content: str # Message Content
    created_at: datetime # Message Creation Date

class Guild:
    """Modela um objeto guild (servidor) mínimo."""
    _id: str # Server ID (Guild ID)
    name: str # Server Name (Guild Name)
    moderating_hystory: int # Number of messages in message_hystory already moderated
    message_hystory: List[Message] # Lista de mensagens do servidor

class Moderation:
    """Modela um objeto de moderação mínimo."""
    bad_author_id: str # User ID (Author ID) of the author of the message that was moderated
    problem: str # Problem found in the messages
    moderated_at: datetime # Date when the messages were moderated 