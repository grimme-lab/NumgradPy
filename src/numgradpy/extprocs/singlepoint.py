"""
Module that contains all functions that are relevant for the single point
calculation, which is required for calculating the gradient of a function.
"""

from __future__ import annotations

from .helpfcts import runexec


def single_point_calculation(
    binaryname: str, arguments: dict[str, str | list[str]]
) -> int:
    """
    Proceeds the single point calculation itself.

    Parameters
    ----------
    binaryname : str
        Name of the binary that is used for the calculation.

    Returns
    -------
    errorcode : int
        Error code of the calculation.
    """

    bin_args = list(arguments["args"])
    print("Proceeding single point calculation...")

    # run preparation of single point input
    outfile = str(arguments["perturbation"]) + ".out"
    errfile = str(arguments["perturbation"]) + ".err"
    e = runexec(binaryname, outfile, errfile, bin_args)

    return e
