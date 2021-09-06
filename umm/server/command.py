import uuid
from typing import List

# TODO: switch to using pydantic model for this


class Command:
    def __init__(
        self,
        command: str,
        tags: List[str],
        id: str = None,
        freq: int = None,
        prompts: List[str] = None,
    ):
        """"""
        assert len(command) > 0, "command length 0"
        assert len(tags) > 0, "tags length 0"
        self.command = command
        self.tags = tags
        self.id = id if id else str(uuid.uuid4())
        self.freq = freq if freq else 0
        self.prompts = prompts if prompts else []
