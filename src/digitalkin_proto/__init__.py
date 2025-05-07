"""digitalkin_proto - Python Generated gRPC client and server interfaces.

This package contains generated Python code from Protocol Buffers and gRPC definitions
for interacting with Digitalkin services.
"""

import os
import sys
from importlib.metadata import PackageNotFoundError, version

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    __version__ = version("digitalkin_proto")
except PackageNotFoundError:
    __version__ = "0.1.10"
