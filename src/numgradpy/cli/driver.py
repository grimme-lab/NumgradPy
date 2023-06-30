"""
Driver for the NumGradPy CLI.
"""

import os
import shutil
from argparse import Namespace

from ..constants import DefaultArguments
from ..extprocs.singlepoint import sp_orca as spo
from ..extprocs.singlepoint import sp_qvszp as spq
from ..gradient.gradients import nuclear_gradient
from ..io import Structure, get_orca_energy, write_tm_energy, write_tm_gradient


class Driver:
    """
    Driver for the NumGradPy CLI.
    """

    prefix_eq = "eq"

    def __init__(self, args: Namespace) -> None:
        """
        Constructor.

        Parameters
        ----------
        args : Namespace
            Command line arguments.
        """

        self.args = args

        controlargs = DefaultArguments()
        config = controlargs.get_config()
        orca_default_args = config["orca"]
        # if key of orca_default_args contains "path", then
        # the value is a path to the binary
        if "path" in orca_default_args:
            # print("Setting new environment variables for ORCA...")
            os.environ["PATH"] = (
                str(orca_default_args["path"]) + ":" + os.environ["PATH"]
            )
            os.environ["LD_LIBRARY_PATH"] = (
                str(orca_default_args["path"]) + ":" + os.environ["LD_LIBRARY_PATH"]
            )
            os.system("export PATH")
            os.system("export LD_LIBRARY_PATH")

    def run(self) -> None:
        """
        Run the driver.
        """

        args = self.args

        # get structure from file
        struc = Structure()
        struc.read_xyz(args.struc)
        # if args.struc corresponds to 'coord', copy 'coord' to 'coord.bak'
        if args.struc == "coord":
            shutil.copy2("coord", "coord.bak")
        if args.verbose:
            print("Structure from file:")
            struc.print_xyz()

        # calculate equilibrium energy
        eq_energy = self.eq_energy(struc)
        print("Equilibrium energy: " + str(eq_energy))

        # write equilibrium energy to file
        write_tm_energy(eq_energy, "energy")

        # calculate nuclear gradient
        gradient = nuclear_gradient(
            struc, args.finitediff, self.prefix_eq, args.verbose
        )

        # print the gradient matrix in nice format
        print("Gradient matrix:")
        for i in range(struc.nat):
            print(
                f"{gradient[i, 0]:10.6f} {gradient[i, 1]:10.6f} {gradient[i, 2]:10.6f}"
            )
        write_tm_gradient(gradient, eq_energy, struc, "gradient")

    def eq_energy(self, eqstruc: Structure) -> float:
        """
        Calculate the equilibrium energy of a structure.
        """

        # delete the following files if they are present
        if os.path.exists(self.prefix_eq + ".gbw"):
            os.remove(self.prefix_eq + ".gbw")
        if os.path.exists(self.prefix_eq + ".densities"):
            os.remove(self.prefix_eq + ".densities")
        Structure.write_xyz(eqstruc, self.prefix_eq + ".xyz", verbose=self.args.verbose)
        e = spq(
            "qvSZP",
            ["--struc", "eq.xyz", "--outname", self.prefix_eq, "--mpi", "4"],
            self.prefix_eq,
        )
        if not e:
            raise RuntimeError("Equilibrium energy calculation failed.")
        e = spo("orca", self.prefix_eq)
        print("Equilibrium energy successfully calculated.")
        energy = get_orca_energy(self.prefix_eq + ".out")
        return energy
