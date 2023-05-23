"""
Module containing standard q-vSZP arguments.
"""

from __future__ import annotations

from pathlib import Path


def get_qvszp_args() -> dict[str, object]:
    """
    Function containing the default q-vSZP arguments.
    """
    # check if the file ".qvSZPrc" exists in the
    # home directory of the user
    # if yes, read the arguments from there
    # if no, use the default arguments
    # if the file exists, but the arguments are not
    # valid, use the default arguments

    # define the default arguments
    args = {
        "basisfile": "/home/marcel/source_rest/qvSZP/basisq",
        "ecpfile": "/home/marcel/source_rest/qvSZP/ecpq",
        "mpi": 1,
        "guess": "hcore",
    }

    # check if the file exists
    qvszprc = Path.home() / ".qvSZPrc"

    if qvszprc.exists():
        # read the arguments from the file
        with open(qvszprc, encoding="UTF-8") as file:
            lines = file.readlines()

        # check if the arguments are valid
        for line in lines:
            if line[0] == "#":
                continue

            value: int | str

            # split the line into key and value
            key, value = line.split("=")

            # remove whitespaces
            key = key.strip()
            value = value.strip()

            # check if the key is valid
            if key not in args.keys():
                continue

            # check if the value is valid
            if key == "mpi":
                try:
                    value = int(value)
                except ValueError:
                    continue
            elif key == "guess":
                if value.lower() not in ["hcore", "pmodel", "patom", "hueckel"]:
                    continue

            # if the value is valid, replace the default value
            args[key] = value

    return args


# Function that fills a list with the elements of a dictionary
# for the default q-vSZP arguments.
def create_arglist(argdict: dict[str, object]) -> list[str]:
    """
    Function that fills a list with the elements of a dictionary
    for the default q-vSZP arguments.
    """
    arglist = []

    for key, value in argdict.items():
        arglist.append("--" + key)
        arglist.append(str(value))

    return arglist
