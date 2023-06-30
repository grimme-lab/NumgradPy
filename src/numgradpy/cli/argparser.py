"""
Parser for command line arguments.
"""

from __future__ import annotations

import argparse


def parser() -> argparse.ArgumentParser:
    """
    Parser for command line arguments.

    Returns
    -------
    parser : argparse.ArgumentParser
        Parser for command line arguments.
    """

    p = argparse.ArgumentParser(description="Calculate the gradient of a function.")

    # define arguments that are passed via a command line flag (e.g. -n)
    p.add_argument(
        "-f",
        "--finitediff",
        type=float,
        help="Finite difference that is used for the calculation.",
        required=True,
    )
    p.add_argument(
        "-b",
        "--binary",
        type=str,
        help="Binary that is used for the calculation.",
        required=True,
    )
    p.add_argument(
        "-s",
        "--struc",
        type=str,
        help="Structure file that is used for the calculation.",
        required=True,
    )
    p.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="Print more information to the console.",
        required=False,
    )

    return p
