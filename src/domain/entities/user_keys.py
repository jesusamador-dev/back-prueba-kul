from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class UserKeys:
    user_id: str
    public_key_1: str
    private_key_1: str
    public_key_2: str
    private_key_2: str
    id: str = str(uuid.uuid4())
    created_at: datetime = field(default_factory=datetime.utcnow)
