"""Version information for digitalkin_proto package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("digitalkin_proto")
except PackageNotFoundError:
    __version__ = "0.2.0.dev4"
