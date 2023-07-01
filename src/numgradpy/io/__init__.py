"""
External procedures
====

This module contains all external procedures that are required for the
calculation of the gradient of a function.
"""

from .parser import get_orca_energy
from .structure import Structure
from .write_output import write_dipole, write_tm_energy, write_tm_gradient
