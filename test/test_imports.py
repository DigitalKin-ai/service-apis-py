"""Basic import tests for the digitalkin_proto package."""

import pytest


def test_import_package():
    """Test that the package can be imported."""
    import digitalkin_proto

    assert digitalkin_proto is not None


def test_submodule_imports():
    """Test importing submodules (if they exist after generation)."""
    # This test will need to be expanded based on actual generated modules
    # The imports below are examples and may need adjusting
    try:
        from digitalkin_proto.digitalkin.module import module_pb2

        assert module_pb2 is not None
    except ImportError:
        pytest.skip("module_pb2 not available, skipping test")

    try:
        from digitalkin_proto.digitalkin.module_registry import registry_pb2

        assert registry_pb2 is not None
    except ImportError:
        pytest.skip("registry_pb2 not available, skipping test")
