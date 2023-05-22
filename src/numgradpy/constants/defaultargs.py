"""
Module containing standard q-vSZP arguments.
"""

from __future__ import annotations


def get_qvszp_args() -> dict[str, object]:
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


# Function that fills a list with the elements of a dictionary
# for the default q-vSZP arguments.
def create_arglist(argdict: dict[str, object]) -> list[str]:
    """
    Function that fills a list with the elements of a dictionary
    for the default q-vSZP arguments.
    """
    arglist = []

    for key, value in argdict.items():
        arglist.append("--" + key)
        arglist.append(str(value))

    return arglist
