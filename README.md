# agentic-mesh-protocol

[![CI](https://github.com/DigitalKin-ai/service-apis-py/actions/workflows/ci.yml/badge.svg)](https://github.com/DigitalKin-ai/service-apis-py/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/agentic-mesh-protocol.svg)](https://pypi.org/project/agentic-mesh-protocol/)
[![Python Version](https://img.shields.io/pypi/pyversions/agentic-mesh-protocol.svg)](https://pypi.org/project/agentic-mesh-protocol/)
[![License](https://img.shields.io/github/license/DigitalKin-ai/service-apis-py)](https://github.com/DigitalKin-ai/service-apis-py/blob/main/LICENSE)

Python gRPC interfaces for the Agentic Mesh Protocol.

## Installation

```bash
pip install agentic-mesh-protocol
```

## Overview

This package provides Python interfaces generated from Agentic Mesh Protocol
Buffer definitions, enabling seamless integration with agentic mesh services via
gRPC.

## Usage

### Basic Import

```python
import agentic_mesh_protocol
from agentic_mesh_protocol.module.v1 import information_pb2, module_service_pb2_grpc
```

### Working with gRPC Services

Example for connecting to a gRPC service:

```python
import grpc
from agentic_mesh_protocol.module.v1 import module_service_pb2_grpc
from agentic_mesh_protocol.module.v1 import information_pb2

# Create a gRPC channel and client stub
channel = grpc.insecure_channel('localhost:50051')
stub = module_service_pb2_grpc.ModuleServiceStub(channel)

# Create a request object
request = information_pb2.GetModuleInputRequest(
    module_id="my-module-id"
)

# Call the service
response = stub.GetModuleInput(request)
print(response)
```

## Development

### Prerequisites

- Python 3.10+
- [uv](https://astral.sh/uv) - Modern Python package management
- [Task](https://taskfile.dev/) - Task runner
- rsync - For copying generated files

Note: `buf` and `protoc` are handled by the submodule via npx, no local installation needed

### Setup Development Environment

```bash
# Clone the repository with submodules
git clone --recurse-submodules https://github.com/DigitalKin-ai/service-apis-py.git
cd service-apis-py

# Setup development environment
task setup

# Or use the quick dev setup command
task dev
```

### Local Installation & Testing

To test the package locally before publishing:

```bash
# Install the package in editable mode
uv pip install -e .

# Or with pip
pip install -e .

# Run the local test script
python test_local.py
```

To test the package in an isolated environment (simulates a fresh install):

```bash
# Using uv (recommended)
uv run --with . --no-project -- python test_local.py

# Or create a fresh venv
python -m venv /tmp/test-amp
source /tmp/test-amp/bin/activate
pip install .
python test_local.py
deactivate
rm -rf /tmp/test-amp
```

### Common Development Tasks

```bash
# Generate Python code from protobuf definitions
task gen

# Build the package
task build

# Run tests
task test

# Format code
task fmt

# Lint code
task lint

# Clean build artifacts
task clean

# Bump version
task bump-version -- patch
task bump-version -- minor
task bump-version -- major
```

### Publishing Process

1. Update code and commit changes
2. Use the GitHub "Create Release" workflow to bump version (patch, minor,
   major)
3. The workflow will automatically create a new release and publish to PyPI

## License

This project is licensed under the terms specified in the LICENSE file.
