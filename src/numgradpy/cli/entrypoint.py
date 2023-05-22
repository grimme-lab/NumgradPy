"""
Entrypoint for command line interface.
"""

from __future__ import annotations

from collections.abc import Sequence

from .argparser import parser
from .driver import Driver


def console_entry_point(argv: Sequence[str] | None = None) -> int:
    # parse arguments
    args = parser().parse_args(argv)
    print(args)

    # run driver
    driver = Driver(args)
    driver.run()

    return 0
