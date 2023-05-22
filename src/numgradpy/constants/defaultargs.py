"""
Module containing standard q-vSZP arguments.
"""

from __future__ import annotations


def qvszp_args() -> dict[str, object]:
    """
    Function containing the default q-vSZP arguments.
    """

    args = {
        "basisfile": "/home/marcel/source_rest/qvSZP/basisq",
        "ecpfile": "/home/marcel/source_rest/qvSZP/ecpq",
        "mpi": 1,
        "guess": "hcore",
    }

    return args
