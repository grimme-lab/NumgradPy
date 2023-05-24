"""
Module that contains all functions that are relevant for the single point
calculation, which is required for calculating the gradient of a function.
"""

from __future__ import annotations

from ..constants import create_arglist, get_qvszp_args
from .helpfcts import runexec


def sp_qvszp(binaryname: str, arguments: list[str], calcname: str) -> int:
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

    qvszp_default_args = get_qvszp_args()
    qvszp_arglist = create_arglist(qvszp_default_args)

    bin_args = qvszp_arglist + arguments

    # run preparation of single point input
    outfile = binaryname + "_numdiff_" + calcname + ".out"
    errfile = binaryname + "_numdiff_" + calcname + ".err"
    e = runexec(binaryname, outfile, errfile, bin_args)

    return e


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
    outfile = binaryname + calcname + ".out"
    errfile = binaryname + calcname + ".err"
    e = runexec(binaryname, outfile, errfile, [calcname + ".inp"])

    return e
