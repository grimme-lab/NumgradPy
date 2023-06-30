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
