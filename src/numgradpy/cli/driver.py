"""
Driver for the NumGradPy CLI.
"""

import subprocess as sp
from argparse import Namespace

from ..extprocs.singlepoint import sp_orca as spo
from ..extprocs.singlepoint import sp_qvszp as spq
from ..gradient.gradients import nuclear_gradient
from ..io import Structure, get_orca_energy, write_tm_energy


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

    def run(self) -> None:
        """
        Run the driver.
        """

        args = self.args

        # get structure from file
        struc = Structure()
        struc.read_xyz(args.struc)
        print("Structure from file:")
        struc.print_xyz()

        # calculate equilibrium energy
        eq_energy = self.eq_energy(struc)
        print("Equilibrium energy: " + str(eq_energy))

        # write equilibrium energy to file
        write_tm_energy(eq_energy, "energy")

        # calculate nuclear gradient
        nuclear_gradient(struc, args.finitediff, self.prefix_eq)

    def eq_energy(self, eqstruc: Structure) -> float:
        """
        Calculate the equilibrium energy of a structure.
        """
        Structure.write_xyz(eqstruc, self.prefix_eq + ".xyz")
        e = spq(
            "qvSZP",
            ["--struc", "eq.xyz", "--outname", self.prefix_eq, "--mpi", "4"],
            self.prefix_eq,
        )
        if not e:
            raise RuntimeError("Equilibrium energy calculation failed.")
        orca_path = (
            sp.run(["which", "orca"], stdout=sp.PIPE, check=True)
            .stdout.decode("utf-8")
            .strip()
        )
        e = spo(orca_path, self.prefix_eq)
        print("Equilibrium energy successfully calculated.")
        energy = get_orca_energy(self.prefix_eq + ".out")
        return energy
