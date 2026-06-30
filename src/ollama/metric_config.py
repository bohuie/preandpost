from dataclasses import dataclass
from typing import Callable


ExpectedValueFunction = Callable[[dict], int]


@dataclass(frozen=True)
class MetricConfig:
    name: str
    expected_value_function: (
        ExpectedValueFunction | None
    ) = None
    validate_against_expected: bool = False



def expected_lines(chunk: dict) -> int:
    physical_lines = chunk.get(
        "physical_lines",
        [],
    )

    if not physical_lines:
        return 0

    return int(
        physical_lines[-1]["line_number"]
    )


LINES_CONFIG = MetricConfig(
    name="lines",
    expected_value_function=expected_lines,
    validate_against_expected=True,
)

COMMENT_LINES_CONFIG = MetricConfig(
    name="comment_lines",
    expected_value_function=None,
    validate_against_expected=False,
)