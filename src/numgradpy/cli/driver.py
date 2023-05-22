"""
Driver for the NumGradPy CLI.
"""

from argparse import Namespace
from multiprocessing import Pool

from ..extprocs.singlepoint import single_point_calculation as spc


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

        outname1 = "struc1"
        outname2 = "struc2"

        # set up list with arguments for single point calculation
        arglist = (
            {
                "perturbation": "xplus",
                "args": [
                    "--struc",
                    "struc1.xyz",
                    "--basisfile",
                    "/home/marcel/source_rest/qvSZP/basisq",
                    "--ecpfile",
                    "/home/marcel/source_rest/qvSZP/ecpq",
                    "--mpi",
                    "1",
                    "--guess",
                    "hcore",
                    "--outname",
                    outname1 + "_q-vSZP.out",
                ],
            },
            {
                "perturbation": "xminus",
                "args": [
                    "--struc",
                    "struc2.xyz",
                    "--basisfile",
                    "/home/marcel/source_rest/qvSZP/basisq",
                    "--ecpfile",
                    "/home/marcel/source_rest/qvSZP/ecpq",
                    "--mpi",
                    "1",
                    "--guess",
                    "hcore",
                    "--outname",
                    outname2 + "_q-vSZP.out",
                ],
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
