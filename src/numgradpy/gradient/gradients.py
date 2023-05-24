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
    for i in range(struc.nat):
        smspqinput = []
        smspoinput = []
        for j in range(3):
            # create structure object for positive perturbation
            struc_modplus = copy.deepcopy(struc)
            struc_modplus.modify_structure(i, j, fdiff)
            struc_modplus.print_xyz()
            counter = 2 * (j + 1) - 1
            prefix = "numdiff_" + str(i) + "_" + str(counter)
            tmpstrucfile = prefix + ".xyz"
            struc_modplus.write_xyz(tmpstrucfile)
            smspoinput.append(("orca", prefix))
            smspqinput.append(
                (
                    "qvSZP",
                    ["--struc", tmpstrucfile, "--outname", prefix],
                    str(counter),
                )
            )
            # create structure object for negative perturbation
            struc_modminus = copy.deepcopy(struc)
            struc_modminus.modify_structure(i, j, -fdiff)
            struc_modminus.print_xyz()
            counter = 2 * (j + 1)
            prefix = "numdiff_" + str(i) + "_" + str(counter)
            tmpstrucfile = prefix + ".xyz"
            struc_modminus.write_xyz(tmpstrucfile)
            smspoinput.append(("orca", prefix))
            smspqinput.append(
                (
                    "qvSZP",
                    ["--struc", tmpstrucfile, "--outname", prefix],
                    str(counter),
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
