"""Test that all generated proto modules can be imported."""


def test_all_proto_imports():
    """Test that all generated proto modules can be imported successfully."""
    # Context service imports
    # Shared packages
    from agentic_mesh_protocol.common.v1 import (
        common_enums_pb2,
    )
    from agentic_mesh_protocol.context.v1 import (
        context_service_pb2,
    )

    # Cost service imports
    from agentic_mesh_protocol.cost.v1 import (
        cost_service_pb2,
    )

    # Filesystem service imports
    from agentic_mesh_protocol.filesystem.v1 import (
        filesystem_service_pb2,
    )

    # Graph service imports (public service and internal admin service)
    from agentic_mesh_protocol.graph.v1 import (
        graph_admin_service_pb2,
        graph_admin_service_pb2_grpc,
        graph_service_pb2,
        graph_service_pb2_grpc,
    )

    # Module service imports
    from agentic_mesh_protocol.module.v1 import (
        module_service_pb2,
    )
    from agentic_mesh_protocol.pagination.v1 import (
        pagination_pb2,
    )

    # Registry service imports
    from agentic_mesh_protocol.registry.v1 import (
        registry_service_pb2,
    )

    # Setup service imports
    from agentic_mesh_protocol.setup.v1 import (
        setup_service_pb2,
    )

    # Storage service imports
    from agentic_mesh_protocol.storage.v1 import (
        storage_service_pb2,
    )

    # User profile service imports
    from agentic_mesh_protocol.user_profile.v1 import (
        user_profile_service_pb2,
    )

    # Verify that the modules have expected attributes (basic sanity check)
    assert hasattr(graph_service_pb2, "DESCRIPTOR")
    assert hasattr(graph_admin_service_pb2, "DESCRIPTOR")
    assert hasattr(graph_service_pb2_grpc, "GraphServiceStub")
    assert hasattr(graph_admin_service_pb2_grpc, "GraphAdminServiceStub")
    assert hasattr(common_enums_pb2, "DESCRIPTOR")
    assert hasattr(pagination_pb2, "DESCRIPTOR")
    assert hasattr(context_service_pb2, "DESCRIPTOR")
    assert hasattr(module_service_pb2, "DESCRIPTOR")
    assert hasattr(registry_service_pb2, "DESCRIPTOR")
    assert hasattr(storage_service_pb2, "DESCRIPTOR")
    assert hasattr(filesystem_service_pb2, "DESCRIPTOR")
    assert hasattr(cost_service_pb2, "DESCRIPTOR")
    assert hasattr(setup_service_pb2, "DESCRIPTOR")
    assert hasattr(user_profile_service_pb2, "DESCRIPTOR")
    assert hasattr(registry_service_pb2, "DESCRIPTOR")
