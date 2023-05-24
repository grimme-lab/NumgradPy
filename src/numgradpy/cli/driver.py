"""
Driver for the NumGradPy CLI.
"""

import sys
from argparse import Namespace
from multiprocessing import Pool

from ..constants import create_arglist, get_qvszp_args
from ..extprocs.singlepoint import single_point_calculation as spc
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

        struc_mod = Structure()
        struc_mod.read_xyz(args.struc)
        struc_mod.modify_structure(0, 0, fdiff)
        print("Perturbed structure:")
        struc_mod.print_xyz()

        print("Original structure:")
        struc.print_xyz()
        print("Perturbed structures:")
        # numerical gradient calculation
        for i in range(struc.nat):
            for j in range(3):
                # perturbation in positive direction
                struc_mod = struc.copy_structure()
                struc_mod.modify_structure(i, j, fdiff)
                struc_mod.print_xyz()
                # perturbation in negative direction
                struc_mod2 = struc.copy_structure()
                struc_mod2.modify_structure(i, j, -fdiff)
                struc_mod2.print_xyz()
                # print the structures

        struc_mod = Structure()
        struc_mod.set_structure(struc.atoms, struc.coordinates)
        # struc_mod.modify_structure(i, j, fdiff)
        # struc_mod.print_xyz()
        outname1 = "struc1"
        outname2 = "struc2"

        qvszp_args = get_qvszp_args()
        qvszp_arglist = create_arglist(qvszp_args)

        arglist_xplus = [
            "--struc",
            "struc1.xyz",
            "--outname",
            outname1 + "_q-vSZP.out",
        ]
        arglist_xplus.extend(qvszp_arglist)
        arglist_xminus = [
            "--struc",
            "struc2.xyz",
            "--outname",
            outname2 + "_q-vSZP.out",
        ]
        arglist_xminus.extend(qvszp_arglist)

        # set up list with arguments for single point calculation
        arglist = (
            {
                "perturbation": "xplus",
                "args": arglist_xplus,
            },
            {
                "perturbation": "xminus",
                "args": arglist_xminus,
            },
        )

        # call the function spc with the binary name "qvSZP"
        # in parallel with multiprocessing
        # and using the different list of arguments in arglist
        with Pool(2) as p:
            p.starmap(spc, [("qvSZP", arg) for arg in arglist])

        # orca_arglist = (
        #    [
        #        "struc1.inp",
        #    ],
        #    [
        #        "struc2.inp",
        #    ],
        # )

        # call the function spc with the binary name "orca"

        # with Pool(2) as p:
        #    p.starmap(spc, [("orca", arg) for arg in orca_arglist])
