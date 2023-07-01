"""
Module that contains all functions that are relevant for the single point
calculation, which is required for calculating the gradient of a function.
"""

from __future__ import annotations

from ..constants import DefaultArguments
from .helpfcts import runexec


def sp_qvszp(
    binaryname: str, arguments: list[str], calcname: str, verbose: bool
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

    controlargs = DefaultArguments()
    config = controlargs.get_config()

    qvszp_default_args = config["qvszp"]
    qvszp_arglist = create_arglist(qvszp_default_args)

    bin_args = qvszp_arglist + arguments

    # run preparation of single point input
    outfile = binaryname + "_" + calcname + ".out"
    errfile = binaryname + "_" + calcname + ".err"
    e = runexec(binaryname, outfile, errfile, bin_args)
    if verbose:
        print("Arguments for ' ", binaryname, " : ", bin_args)

    return e


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


def sp_orca(binaryname: str, calcname: str) -> int:
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

    # run preparation of single point input
    outfile = calcname + ".out"
    errfile = calcname + ".err"
    e = runexec(binaryname, outfile, errfile, [calcname + ".inp"])

    return e
