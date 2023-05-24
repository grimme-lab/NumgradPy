"""
Module to write energy and gradient to a file.
"""

from __future__ import annotations


def write_tm_energy(energy: float, outfile: str) -> None:
    """
    Write the energy to a file.

    Parameters
    ----------
    energy : float
        Energy in Hartree.
    outfile : str
        Name of the output file.
    """

    with open(outfile, "w", encoding="UTF-8") as f:
        print("$energy      SCF               SCFKIN            SCFPOT", file=f)
        print(f"     1 {energy:.12f}", file=f)
        print("$end", file=f)
