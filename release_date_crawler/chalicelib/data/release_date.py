from dataclasses import dataclass
from datetime import date


@dataclass
class ReleaseDateData:
    title: str=""
    release_date: date=None

