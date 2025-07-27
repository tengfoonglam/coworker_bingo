from dataclasses import dataclass


class BingoSheetGenerator:
    @dataclass
    class Config:
        participant: str
        participants: set[str]
        specific_facts: dict[str, list[str]]
        generic_facts: list[str]

    def __init__(self) -> None:
        pass
