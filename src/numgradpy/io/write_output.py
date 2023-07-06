"""
Module to write energy and gradient to a file.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ..io import Structure


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


def write_tm_gradient(
    gradient: npt.NDArray[np.float64], sp_energy: float, struc: Structure, outfile: str
) -> None:
    """
    Write the gradient to a file.

    Parameters
    ----------
    gradient : npt.NDArray[np.float64]
        Gradient in Hartree/Bohr.
    sp_energy : float
        Single point energy in Hartree.
    struc : Structure
        Structure object.
    outfile : str
        Name of the output file.
    """

    # calculate |dE/dxyz| of the gradient (norm of the gradient)
    # as a single number for the full gradient
    norm = np.linalg.norm(gradient)

    with open(outfile, "w", encoding="UTF-8") as f:
        print("$grad        cartesian gradients", file=f)
        print(
            f"  cycle = 1   SCF energy = {sp_energy:16.10f} \
|dE/dxyz| = {norm:16.10f}",
            file=f,
        )
        for i in range(struc.nat):
            print(
                f"{struc.coordinates[i, 0]:18.12f} \
{struc.coordinates[i, 1]:18.12f} \
{struc.coordinates[i, 2]:18.12f} {struc.atoms[i]}",
                file=f,
            )
        for i in range(gradient.shape[0]):
            print(
                f"{gradient[i, 0]:18.12f} \
{gradient[i, 1]:18.12f} \
{gradient[i, 2]:18.12f}",
                file=f,
            )
        print("$end", file=f)


def write_dipole(dipole: npt.NDArray[np.float64], outfile: str) -> None:
    """
    Write the dipole moment to a file.

    Parameters
    ----------
    dipole : npt.NDArray[np.float64]
        Dipole moment in Debye.
    outfile : str
        Name of the output file.
    """

    with open(outfile, "w", encoding="UTF-8") as f:
        print("$dipole", file=f)
        print(
            f"{dipole[0]:18.12f} {dipole[1]:18.12f} {dipole[2]:18.12f}",
            file=f,
        )


def write_polarizability(polarizability: npt.NDArray[np.float64], outfile: str) -> None:
    """
    Write the polarizability to a file.

    Parameters
    ----------
    polarizability : npt.NDArray[np.float64]
        Polarizability in Bohr^3.
    outfile : str
        Name of the output file.
    """

    with open(outfile, "w", encoding="UTF-8") as f:
        print("$polarizability", file=f)
        print(
            f"{polarizability[0,0]:18.12f} \
{polarizability[0,1]:18.12f} \
{polarizability[0,2]:18.12f}",
            file=f,
        )
        print(
            f"{polarizability[1,0]:18.12f} \
{polarizability[1,1]:18.12f} \
{polarizability[1,2]:18.12f}",
            file=f,
        )
        print(
            f"{polarizability[2,0]:18.12f} \
{polarizability[2,1]:18.12f} \
{polarizability[2,2]:18.12f}",
            file=f,
        )
