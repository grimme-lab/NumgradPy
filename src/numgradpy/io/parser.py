"""
Module to parse outputs from ORCA into NumGradPy's internal data structures.
"""

from __future__ import annotations


def get_orca_energy(outfile: str) -> float:
    """
    Get the energy from an ORCA output file.

    Parameters
    ----------
    outfile : str
        Name of the ORCA output file.

    Returns
    -------
    energy : float
        Energy in Hartree.
    """

    with open(outfile, encoding="UTF-8") as f:
        lines = f.readlines()
    energy = 0.0
    energyfound = False
    for line in lines:
        if "FINAL SINGLE POINT ENERGY" in line:
            energy = float(line.split()[4])
            energyfound = True
    if not energyfound:
        raise RuntimeError("Energy not found in ORCA output file.")

    return energy
