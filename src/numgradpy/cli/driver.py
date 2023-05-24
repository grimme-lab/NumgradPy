"""
Driver for the NumGradPy CLI.
"""

import copy
import sys
from argparse import Namespace
from multiprocessing import Pool

from ..extprocs.singlepoint import sp_orca as spo
from ..extprocs.singlepoint import sp_qvszp as spq
from ..io import Structure


class Driver:
    """
    Driver for the NumGradPy CLI.
    """

    def __init__(self, args: Namespace) -> None:
        """
        Constructor.

        Parameters
        ----------
        args : Namespace
            Command line arguments.
        """

        self.args = args

    def run(self) -> None:
        """
        Run the driver.
        """

        args = self.args
        fdiff = args.finitediff
        fdiff = 0.1

        # get structure from file
        struc = Structure()
        struc.read_xyz(args.struc)
        print("Structure from file:")
        struc.print_xyz()

        # numerical gradient calculation
        argslist: list[list[str]] = []
        perturbation: list[str] = []
        orcainpname: list[str] = []
        for i in range(struc.nat):
            argslist = []
            perturbation = []
            orcainpname = []
            for j in range(3):
                # create structure object for positive perturbation
                struc_modplus = copy.deepcopy(struc)
                struc_modplus.modify_structure(i, j, fdiff)
                struc_modplus.print_xyz()
                counter = 2 * (j + 1) - 1
                prefix = "numdiff_" + str(i) + "_" + str(counter)
                tmpstrucfile = prefix + ".xyz"
                struc_modplus.write_xyz(tmpstrucfile)
                perturbation.append(str(counter))
                argslist.append(["--struc", tmpstrucfile, "--outname", prefix])
                orcainpname.append(prefix)
                # create structure object for negative perturbation
                struc_modminus = copy.deepcopy(struc)
                struc_modminus.modify_structure(i, j, -fdiff)
                struc_modminus.print_xyz()
                counter = 2 * (j + 1)
                prefix = "numdiff_" + str(i) + "_" + str(counter)
                tmpstrucfile = prefix + ".xyz"
                struc_modminus.write_xyz(tmpstrucfile)
                argslist.append(["--struc", tmpstrucfile, "--outname", prefix])
                perturbation.append(str(counter))
                orcainpname.append(prefix)

            with Pool(6) as p:
                p.starmap(
                    spq,
                    [
                        ("qvSZP", arg, perturb)
                        for arg, perturb in zip(argslist, perturbation)
                    ],
                )

            with Pool(6) as p:
                p.starmap(
                    spo,
                    [("orca", orcainp) for orcainp in orcainpname],
                )

        print(argslist)
