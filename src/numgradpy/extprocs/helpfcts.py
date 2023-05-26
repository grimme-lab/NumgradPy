"""
Module that contains helper functions interacting with the OS and other processes.
"""

import errno
import os
import subprocess as sp
import sys


def silentremove(*args: str) -> bool:
    for filename in args:
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    return True


def checkifinpath(executable: str) -> str:
    # if output is empty, executable is not in PATH -> FileNotFoundError
    try:
        p = sp.run(["which", executable], stdout=sp.PIPE, stderr=sp.PIPE, check=True)
    except sp.CalledProcessError as e:
        raise FileNotFoundError(f"'{executable}' is not in PATH") from e

    if p.stdout == b"":
        raise FileNotFoundError(f"'{executable}' is not in PATH")
    else:
        fullpath = p.stdout.decode("utf-8").strip()

    return fullpath


def runexec(executable: str, outfile: str, errfile: str, arglist: list[str]) -> bool:
    fpath = checkifinpath(executable)
    with open(outfile, "w", encoding="UTF-8") as stdout_file, open(
        errfile, "w", encoding="UTF-8"
    ) as stderr_file:
        try:
            # inserting all entries of arglist as
            # arguments for the executable call in sp.run()
            sp.run([fpath, *arglist], stdout=stdout_file, stderr=sp.PIPE, check=True)
        except sp.CalledProcessError as error:
            print(f"An error occurred: {error}")
            print(f"Error output:\n{error.stderr.decode('utf-8')}")
            stderr_file.write(error.stderr.decode("utf-8"))
            sys.exit(1)
    # return exit code of executable
    return True
