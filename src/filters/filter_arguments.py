from dataclasses import dataclass


@dataclass
class FilterArguments:
    filter_type: str
    order: int
    b_type: str
    cutoff_frequency: float
    other_cutoff_frequency: float | None = None
    analog: bool = False
