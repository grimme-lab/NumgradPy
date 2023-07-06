"""
Module in which the gradient functions are defined.
"""

from __future__ import annotations

import copy
import shutil
from multiprocessing import Pool

import numpy as np
import numpy.typing as npt

from ..extprocs.singlepoint import sp_orca as spo
from ..extprocs.singlepoint import sp_qvszp as spq
from ..io import Structure, get_orca_energy


def nuclear_gradient(
    struc: Structure,
    fdiff: float,
    startgbw: str,
    verbose: bool,
) -> npt.NDArray[np.float64]:
    # set up a numpy tensor for the gradient
    gradient = np.zeros((struc.nat, 3), dtype=np.float64)
    # numerical gradient calculation
    smspoinput: list[tuple[str, str]] = []
    # smspqinput: list[tuple[str, list[str], str]] = []
    counter = 0
    for i in range(struc.nat):
        # smspqinput = []
        smspoinput = []
        prefix = "numdiff_" + str(i + 1) + "_"
        for j in range(3):
            # create structure object for positive perturbation
            struc_mod = copy.deepcopy(struc)
            struc_mod.modify_structure(i, j, fdiff, verbose=verbose)
            if verbose:
                struc_mod.print_xyz()
            counter = 2 * (j + 1) - 1
            tmpstrucfile = prefix + str(counter) + ".xyz"
            struc_mod.write_xyz(tmpstrucfile, verbose=verbose)
            es = spq(
                "qvSZP",
                ["--struc", tmpstrucfile, "--outname", prefix + str(counter)],
                str(counter),
                verbose=verbose,
            )
            if not es:
                raise RuntimeError("Single point calculation failed.")
            # create structure object for negative perturbation
            struc_mod.modify_structure(i, j, -2 * fdiff, verbose=verbose)
            if verbose:
                struc_mod.print_xyz()
            counter = 2 * (j + 1)
            tmpstrucfile = prefix + str(counter) + ".xyz"
            struc_mod.write_xyz(tmpstrucfile, verbose=verbose)
            es = spq(
                "qvSZP",
                ["--struc", tmpstrucfile, "--outname", prefix + str(counter)],
                str(counter),
                verbose=verbose,
            )
            if not es:
                raise RuntimeError("Single point calculation failed.")

        if counter != 6:
            raise RuntimeError("Something went wrong with the gradient calculation.")

        # prepare arguments for single point calculations
        for k in range(6):
            prefix = "numdiff_" + str(i + 1) + "_" + str(k + 1)
            # smspqinput.append(
            #     (
            #         "qvSZP",
            #         ["--struc", prefix + ".xyz", "--outname", prefix],
            #         str(k + 1),
            #     )
            # )
            smspoinput.append(("orca", prefix))
            # copy the existing GBW file to the new GBW file
            shutil.copy2(startgbw + ".gbw", prefix + ".gbw")

        # run single point calculations of qvSZP
        # with Pool(6) as p:
        #     e = p.starmap(spq, smspqinput)
        #     if not all(e):
        #         raise RuntimeError(
        #             "Single point calculation failed. Check the output files."
        #         )

        # run single point calculations of ORCA
        with Pool(6) as p:
            el = p.starmap(spo, smspoinput)
            if not all(el):
                raise RuntimeError(
                    "Single point calculation failed. Check the output files."
                )

        for j in range(3):
            counter = 2 * (j + 1) - 1
            fname = "numdiff_" + str(i + 1) + "_" + str(counter) + ".out"
            eplus = get_orca_energy(fname)
            counter = 2 * (j + 1)
            fname = "numdiff_" + str(i + 1) + "_" + str(counter) + ".out"
            eminus = get_orca_energy(fname)
            # gradient = (eplus - eminus) / (2 * fdiff)
            gradient[i, j] = (eplus - eminus) / (2 * fdiff)
            print(
                f"Gradient for atom {i + 1} and coordinate {j + 1}: \
{gradient[i, j]:14.8f}"
            )

    return gradient


def efield_gradient(
    strucfile: str,
    fdiff: float,
    startgbw: str,
    verbose: bool,
    extefield: npt.NDArray[np.float64] = np.zeros((3), dtype=np.float64),
) -> npt.NDArray[np.float64]:
    # set up a numpy tensor for the electric field gradient -> dipole moment
    if verbose:
        print("External electric field:")
        print(f"{extefield[0]:10.6f} {extefield[1]:10.6f} {extefield[2]:10.6f}")
    dipole = np.zeros((3), dtype=np.float64)
    smspoinput: list[tuple[str, str]] = []
    for j in range(3):
        for i in range(2):
            efield = copy.deepcopy(extefield)
            if i == 0:
                efield[j] = efield[j] + fdiff
            else:
                efield[j] = efield[j] - fdiff
            if verbose:
                print("Effective electric field for dipole moment calculation:")
                print(f"{efield[0]:10.6f} {efield[1]:10.6f} {efield[2]:10.6f}")
            es = spq(
                "qvSZP",
                [
                    "--struc",
                    strucfile,
                    "--outname",
                    "efielddiff_" + str(j + 1) + "_" + str(i + 1),
                    "--efield",
                    str(efield[0]),
                    str(efield[1]),
                    str(efield[2]),
                ],
                str(2 * j + i + 1),
                verbose=verbose,
            )
            if not es:
                raise RuntimeError("Single point calculation failed.")
            smspoinput.append(
                (
                    "orca",
                    "efielddiff_" + str(j + 1) + "_" + str(i + 1),
                )
            )
            # copy the existing GBW file to the new GBW file
            shutil.copy2(
                startgbw + ".gbw",
                "efielddiff_" + str(j + 1) + "_" + str(i + 1) + ".gbw",
            )

    # run single point calculations of ORCA
    with Pool(6) as p:
        el = p.starmap(spo, smspoinput)
        if not all(el):
            raise RuntimeError(
                "Single point calculation failed. Check the output files."
            )

    for j in range(3):
        fname = "efielddiff_" + str(j + 1) + "_1.out"
        eplus = get_orca_energy(fname)
        fname = "efielddiff_" + str(j + 1) + "_2.out"
        eminus = get_orca_energy(fname)
        dipole[j] = -(eplus - eminus) / (
            2 * fdiff
        )  # minus sign because of the definition of the dipole moment

    return dipole


def dipole_gradient(
    strucfile: str,
    fdiff: float,
    startgbw: str,
    verbose: bool,
) -> npt.NDArray[np.float64]:
    dipmomdiff = 0.5 * fdiff
    # set up a numpy tensor for the electric field gradient -> dipole moment
    alpha = np.zeros((3, 3), dtype=np.float64)
    for j in range(3):
        extefield = np.zeros((3), dtype=np.float64)
        extefield[j] = fdiff
        dipplus = efield_gradient(strucfile, dipmomdiff, startgbw, verbose, extefield)
        extefield[j] = -fdiff
        dipminus = efield_gradient(strucfile, dipmomdiff, startgbw, verbose, extefield)
        alpha[j, :] = (dipplus - dipminus) / (2 * fdiff)

    return alpha
