"""
Module to parse outputs from ORCA into NumGradPy's internal data structures.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


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


def get_orca_dipolemoment(outfile: str) -> npt.NDArray[np.float64]:
    """
    Get the dipole moment from an ORCA output file.

    Parameters
    ----------
    outfile : str
        Name of the ORCA output file.

    Returns
    -------
    dipolemoment : float
        Dipole moment in Debye.
    """
    dipolemom: npt.NDArray[np.float64] = np.zeros((), dtype=np.float64)

    print(outfile)
    with open(outfile, encoding="UTF-8") as f:
        lines = f.readlines()
    dipolemomentfound = False
    for line in lines:
        if "Total Dipole moment" in line:
            # MM: the following code applies only to '< prefix >_properties.txt'
            # dipole moment entries begin two lines later
            dipolemom = np.array(
                [
                    float(lines[lines.index(line) + 2].split()[1]),
                    float(lines[lines.index(line) + 3].split()[1]),
                    float(lines[lines.index(line) + 4].split()[1]),
                ]
            )
            # MM: the following code applies only to 'orca.out'
            # dipolemom = np.array(
            #     [
            #         float(line.split()[4]),
            #         float(line.split()[5]),
            #         float(line.split()[6]),
            #     ]
            # )
            dipolemomentfound = True
    if not dipolemomentfound:
        raise RuntimeError("Dipole moment not found in ORCA output file.")

    return dipolemom
