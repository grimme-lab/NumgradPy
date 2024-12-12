"""
Module containing the default arguments for the different programs.
"""

from __future__ import annotations

from pathlib import Path


class DefaultArguments:
    """
    Class that contains the default arguments for the different programs.
    """

    defargs: dict[str, dict[str, object]]

    def __init__(self) -> None:
        self.defargs = {"qvszp": self.qvszp_def_args(), "orca": {}}

    def get_config(self) -> dict[str, dict[str, object]]:
        """
        Function returning the overall control dictionary.
        """
        numgradpyrc = Path.home() / ".numgradpyrc"

        if numgradpyrc.exists():
            self.read_config_from_file(numgradpyrc)

        return self.defargs

    def read_config_from_file(self, numgradpyrc: Path) -> None:
        """
        Read the arguments from the configuration file.
        """
        with open(numgradpyrc, encoding="UTF-8") as file:
            lines = file.readlines()

        dictkey = ""
        for line in lines:
            if line[0] == "#":
                continue
            if line.strip().lower() == "$qvszp":
                dictkey = "qvszp"
                continue
            elif line.strip().lower() == "$orca":
                dictkey = "orca"
                continue
            elif line.strip().lower() == "$end":
                return

            if dictkey not in self.defargs:
                raise ValueError("Invalid program name in ~/.numgradpyrc.")

            key, value = line.split("=")
            key = key.strip()
            value = value.strip()
            self.check_argument(dictkey, key, value)
            self.defargs[dictkey][key] = value

    def check_argument(self, program: str, key: str, value: str | int | float) -> None:
        if program == "qvszp":
            qvszp_defargs = self.qvszp_def_args()
            # if key not in qvszp_defargs: # don't need this check, prevents user-defined arguments that are not in the default arguments
            #     raise ValueError("Invalid argument name in ~/.numgradpyrc.")

            if key == "mpi":
                try:
                    value = int(value)
                except ValueError as exc:
                    raise ValueError(
                        "Value for 'mpi' must be an integer in 'numgradpyrc'."
                    ) from exc
            elif key == "guess":
                valid_guesses = ["hcore", "pmodel", "patom", "hueckel"]
                try:
                    value = str(value)
                except ValueError as exc:
                    raise ValueError(
                        f"Value for 'guess' must be one of\
 {valid_guesses} in 'numgradpyrc'."
                    ) from exc
                if value.lower() not in valid_guesses:
                    raise ValueError(
                        f"Value for 'guess' must be one of\
 {valid_guesses} in 'numgradpyrc'."
                    )

    def qvszp_def_args(self) -> dict[str, str | object]:
        qvszp_defargs = {
            "bfile": "/home/marcel/source_rest/qvSZP/q-vSZP_basis/basisq",
            "efile": "/home/marcel/source_rest/qvSZP/q-vSZP_basis/ecpq",
            "mpi": 1,
            "guess": "PModel",
            "defgrid": 3,
            "conv": "VeryTightSCF",
        }
        return qvszp_defargs
