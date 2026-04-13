"""Version information for agentic_mesh_protocol package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("agentic-mesh-protocol")
except PackageNotFoundError:
    __version__ = "1.0.0.dev0"
