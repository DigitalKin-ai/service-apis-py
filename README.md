# digitalkin_proto

[![CI](https://github.com/DigitalKin-ai/service-apis-py/actions/workflows/ci.yml/badge.svg)](https://github.com/DigitalKin-ai/service-apis-py/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/digitalkin_proto.svg)](https://pypi.org/project/digitalkin_proto/)
[![Python Version](https://img.shields.io/pypi/pyversions/digitalkin_proto.svg)](https://pypi.org/project/digitalkin_proto/)
[![License](https://img.shields.io/github/license/DigitalKin-ai/service-apis-py)](https://github.com/DigitalKin-ai/service-apis-py/blob/main/LICENSE)

Python Generated gRPC client and server interfaces from Digitalkin's service
APIs.

## Installation

```bash
pip install digitalkin_proto
```

## Overview

This package provides Python interfaces generated from Digitalkin's Protocol
Buffer definitions, enabling seamless integration with Digitalkin services via
gRPC.

## Usage

### Basic Import

```python
import digitalkin_proto
from digitalkin_proto.digitalkin.module.v1 import module_pb2, module_service_pb2_grpc
```

### Working with gRPC Services

Example for connecting to a gRPC service:

```python
import grpc
from digitalkin_proto.digitalkin.module.v1 import module_service_pb2_grpc
from digitalkin_proto.digitalkin.module.v1 import module_pb2

# Create a gRPC channel and client stub
channel = grpc.insecure_channel('localhost:50051')
stub = module_service_pb2_grpc.ModuleServiceStub(channel)

# Create a request object
request = module_pb2.YourRequestType(
    field1="value1",
    field2="value2"
)

# Call the service
response = stub.YourServiceMethod(request)
print(response)
```

## Development

### Prerequisites

- Python 3.10+
- [uv](https://astral.sh/uv) - Modern Python package management
- [buf](https://buf.build/docs/installation) - Protocol buffer toolkit
- [protoc](https://grpc.io/docs/protoc-installation/) - Protocol Buffers
  compiler
- [Task](https://taskfile.dev/) - Task runner

### Setup Development Environment

```bash
# Clone the repository with submodules
git clone --recurse-submodules https://github.com/DigitalKin-ai/service-apis-py.git
cd service-apis-py

# Setup development environment and activate the venv
task setup-dev
source .venv/bin/activate

```

### Common Development Tasks

```bash
# Generate Python code from protobuf definitions
task gen-proto

# Build the package
task build-package

# Run tests
task run-tests

# Format code
task format

# Lint code
task lint

# Clean build artifacts
task clean

# Bump version
task bump-version -- major
task bump-version -- minor
task bump-version -- patch
```

### Publishing Process

1. Update code and commit changes
2. Use the GitHub "Create Release" workflow to bump version (patch, minor,
   major)
3. The workflow will automatically create a new release and publish to PyPI

## License

This project is licensed under the terms specified in the LICENSE file.
