"""
Driver for the NumGradPy CLI.
"""

from argparse import Namespace

from ..gradient.gradients import nuclear_gradient
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

        # get structure from file
        struc = Structure()
        struc.read_xyz(args.struc)
        print("Structure from file:")
        struc.print_xyz()

        # calculate nuclear gradient
        nuclear_gradient(struc, args.finitediff)
