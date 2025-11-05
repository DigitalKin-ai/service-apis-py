"""Test that all generated proto modules can be imported."""


def test_all_proto_imports():
    """Test that all generated proto modules can be imported successfully."""
    # Module service imports
    # Cost service imports
    from digitalkin_proto.agentic_mesh_protocol.cost.v1 import (
        cost_service_pb2,
    )

    # Filesystem service imports
    from digitalkin_proto.agentic_mesh_protocol.filesystem.v1 import (
        filesystem_service_pb2,
    )
    from digitalkin_proto.agentic_mesh_protocol.module.v1 import (
        module_service_pb2,
    )

    # Module registry service imports
    from digitalkin_proto.agentic_mesh_protocol.module_registry.v1 import (
        module_registry_service_pb2,
    )

    # Setup service imports
    from digitalkin_proto.agentic_mesh_protocol.setup.v1 import (
        setup_service_pb2,
    )

    # Storage service imports
    from digitalkin_proto.agentic_mesh_protocol.storage.v1 import (
        storage_service_pb2,
    )

    # User profile service imports
    from digitalkin_proto.agentic_mesh_protocol.user_profile.v1 import (
        user_profile_service_pb2,
    )

    # Verify that the modules have expected attributes (basic sanity check)
    assert hasattr(module_service_pb2, "DESCRIPTOR")
    assert hasattr(module_registry_service_pb2, "DESCRIPTOR")
    assert hasattr(storage_service_pb2, "DESCRIPTOR")
    assert hasattr(filesystem_service_pb2, "DESCRIPTOR")
    assert hasattr(cost_service_pb2, "DESCRIPTOR")
    assert hasattr(setup_service_pb2, "DESCRIPTOR")
    assert hasattr(user_profile_service_pb2, "DESCRIPTOR")
