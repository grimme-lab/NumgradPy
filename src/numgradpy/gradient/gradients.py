"""
Module in which the gradient functions are defined.
"""

from __future__ import annotations

import copy
from multiprocessing import Pool

from ..extprocs.singlepoint import sp_orca as spo
from ..extprocs.singlepoint import sp_qvszp as spq
from ..io import Structure


def nuclear_gradient(struc: Structure, fdiff: float) -> None:
    # numerical gradient calculation
    smspoinput: list[tuple[str, str]] = []
    smspqinput: list[tuple[str, list[str], str]] = []
    counter = 0
    for i in range(struc.nat):
        smspqinput = []
        smspoinput = []
        prefix = "numdiff_" + str(i + 1) + "_"
        for j in range(3):
            # create structure object for positive perturbation
            struc_mod = copy.deepcopy(struc)
            struc_mod.modify_structure(i, j, fdiff)
            struc_mod.print_xyz()
            counter = 2 * (j + 1) - 1
            tmpstrucfile = prefix + str(counter) + ".xyz"
            struc_mod.write_xyz(tmpstrucfile)
            # create structure object for negative perturbation
            struc_mod.modify_structure(i, j, -2 * fdiff)
            struc_mod.print_xyz()
            counter = 2 * (j + 1)
            tmpstrucfile = prefix + str(counter) + ".xyz"
            struc_mod.write_xyz(tmpstrucfile)

        if counter != 6:
            raise RuntimeError("Something went wrong with the gradient calculation.")
        for k in range(6):
            prefix = "numdiff_" + str(i + 1) + "_" + str(k + 1)
            smspoinput.append(("orca", prefix))
            smspqinput.append(
                (
                    "qvSZP",
                    ["--struc", prefix + ".xyz", "--outname", prefix],
                    str(k + 1),
                )
            )
        with Pool(6) as p:
            e = p.starmap(spq, smspqinput)
            if not all(e):
                raise RuntimeError(
                    "Single point calculation failed. Check the output files."
                )

        with Pool(6) as p:
            e = p.starmap(spo, smspoinput)
            if not all(e):
                raise RuntimeError(
                    "Single point calculation failed. Check the output files."
                )
