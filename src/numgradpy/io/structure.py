"""
Define a class for storing, reading and writing the structure of a molecule.
First, we implement only the XYZ file format.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


class Structure:
    """
    Define a class for storing, reading and writing the structure of a molecule.
    First, we implement only the XYZ file format.
    """

    def __init__(self) -> None:
        """
        Initialize the Structure class.

        Parameters
        ----------
        filename : str
            Name of the file that contains the structure.

        Returns
        -------
        None
        """

        self.filename: str = ""
        self.filetype: str = ""
        self.atoms: list[str] = []
        self.coordinates: npt.NDArray[np.float64] = np.zeros((), dtype=np.float64)

    def read_xyz(self, filename: str) -> tuple[list[str], npt.NDArray[np.float64]]:
        """
        Read the structure from an XYZ file.

        Returns
        -------
        atoms : list[str]
            List of all atoms in the structure.
        coordinates : np.ndarray
            Array of all coordinates in the structure.
        """
        self.filename = filename
        self.filetype = self.filename.split(".")[-1]

        if self.filetype != "xyz":
            raise ValueError("Filetype not supported.")

        coordinates = []

        with open(self.filename, encoding="UTF-8") as file:
            lines = file.readlines()

        for line in lines[2:]:
            self.atoms.append(line.split()[0])
            coordinates.append([float(x) for x in line.split()[1:]])

        self.coordinates = np.array(coordinates)
        return self.atoms, self.coordinates

    # function that sets up an instance of the Structure class with given
    # atoms and coordinates
    def set_structure(
        self, atoms: list[str], coordinates: npt.NDArray[np.float64]
    ) -> None:
        """
        Set up the structure.

        Parameters
        ----------
        atoms : list[str]
            List of all atoms in the structure.
        coordinates : np.ndarray
            Array of all coordinates in the structure.

        Returns
        -------
        None
        """

        self.atoms = atoms
        self.coordinates = coordinates

    def write_xyz(self, newfilename: str) -> None:
        """
        Write the structure to an XYZ file.

        Parameters
        ----------
        atoms : list[str]
            List of all atoms in the structure.
        coordinates : np.ndarray
            Array of all coordinates in the structure.

        Returns
        -------
        None
        """

        with open(newfilename, "w", encoding="UTF-8") as file:
            file.write(f"{len(self.atoms)}\n\n")
            # write the structure to the file
            # and use the ndarray data type for the coordinates
            # NOTE: self.coordinates is a numpy array
            for atom, coordinate in zip(self.atoms, self.coordinates):
                file.write(
                    f"{atom:2s} {coordinate[0]:14.8f}\
 {coordinate[1]:14.8f} {coordinate[2]:14.8f}\n"
                )

    def get_atoms(self) -> list[str]:
        """
        Return the atoms of the structure.

        Returns
        -------
        atoms : list[str]
            List of all atoms in the structure.
        """

        return self.atoms

    def get_coordinates(self) -> npt.NDArray[np.float64]:
        """
        Return the coordinates of the structure.

        Returns
        -------
        coordinates : np.ndarray
            Array of all coordinates in the structure.
        """

        return self.coordinates

    def print_xyz(self) -> None:
        """
        Print the structure in XYZ format.

        Returns
        -------
        None
        """

        print(f"{len(self.atoms)}\n")
        for atom, coordinate in zip(self.atoms, self.coordinates):
            print(
                f"{atom:2s} {coordinate[0]:14.8f}\
 {coordinate[1]:14.8f} {coordinate[2]:14.8f}"
            )

    # function for modifying the structure by adding or subtracting
    # a small value to a variable coordinate of a single atom
    def modify_structure(self, atom: int, coordinate: int, value: float) -> None:
        """
        Modify the structure by adding or subtracting a small value
        to a variable coordinate of a single atom.

        Parameters
        ----------
        atom : int
            Index of the atom to be modified.
        coordinate : int
            Index of the coordinate to be modified.
        value : float
            Value to be added or subtracted.

        Returns
        -------
        None
        """

        self.coordinates[atom][coordinate] = self.coordinates[atom][coordinate] + value
