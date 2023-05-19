"""
Entrypoint for command line interface.
"""

from __future__ import annotations

from collections.abc import Sequence

from .argparser import parser

from ..extprocs.singlepoint import single_point_calculation as spc


def console_entry_point(argv: Sequence[str] | None = None) -> int:
    # parse arguments
    args = parser().parse_args(argv)
    print(args)

    # print(square(args.number))
    spc("binaryname", ["arguments"])

    return 0
