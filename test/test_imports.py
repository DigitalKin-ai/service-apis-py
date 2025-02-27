"""Basic import tests for the digitalkin_proto package."""


def test_import_package():
    """Test that the package can be imported."""
    import digitalkin_proto

    assert digitalkin_proto is not None
    print(f"Success! Version: {digitalkin_proto.__version__}")


def test_submodule_imports():
    """Test importing submodules (if they exist after generation)."""
    from digitalkin_proto.digitalkin.module.v1 import module_service_pb2_grpc

    assert module_service_pb2_grpc is not None

    from digitalkin_proto.digitalkin.module_registry.v1 import module_registry_service_pb2_grpc

    assert module_registry_service_pb2_grpc is not None
