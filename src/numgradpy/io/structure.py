"""
Define a class for storing, reading and writing the structure of a molecule.
First, we implement only the XYZ file format.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ..constants import AA2AU


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
        self.nat: int = 0
        self.atoms: list[str] = []
        self.coordinates: npt.NDArray[np.float64] = np.zeros((), dtype=np.float64)

    def read_xyz(self, filename: str) -> tuple[int, list[str], npt.NDArray[np.float64]]:
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

        coordinates: list[list[float]] = []

        with open(self.filename, encoding="UTF-8") as file:
            lines = file.readlines()

        self.nat = int(lines[0].split()[0])
        for line in lines[2:]:
            self.atoms.append(line.split()[0])
            coordinates.append([float(x) for x in line.split()[1:]])

        if len(coordinates) != self.nat:
            raise ValueError("Number of atoms does not match number of coordinates.")

        # convert the whole coordinates array to atomic units
        self.coordinates = np.array(coordinates) * AA2AU
        return self.nat, self.atoms, self.coordinates

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
        self.nat = len(atoms)
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
                    f"{atom:2s} {(coordinate[0] / AA2AU ):14.8f}\
 {(coordinate[1] / AA2AU ):14.8f} {(coordinate[2] / AA2AU ):14.8f}\n"
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
        Print the structure in atomic units (coord) format.

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

        print(f"Modify atom {atom} coordinate {coordinate} by {value}.")

        # check if the atom index is valid
        if atom < 0 or atom > self.nat:
            raise ValueError("Atom index out of bounds.")
        self.coordinates[atom][coordinate] = self.coordinates[atom][coordinate] + value

        return None
