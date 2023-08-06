# -*- mode:python; eval: (blacken-mode) -*-
"""
Runs Airspeed Velocity (asv) benchmarks in a Bubblewrap sandbox.
"""

__version = "0.2"

if "dev" in __version:
    from ._version import get_dev_version_suffix

    __version += get_dev_version_suffix(__version)
    del get_dev_version_suffix

__version__ = __version
