# service-apis-py

## Usage

### Create and activate venv

```sh
task venv
source .venv/bin/activate
```

### Generate Python code from protobuf

The command will update the submodule version of service-apis, update the proto dep and generate the desire Python code.

```sh
task gen-proto
```

### Generate the Python package 'service-apis-py'

The command generate the Python venv, download the dependencies and build the package.

```sh
task generate-package
```

### Publish and test the package

The command push the package to the PyPI's test env and test it.

```sh
task test-publish
```

### All-in-one

Execute all the commands

```sh
task all
```

## Installation

Ensure [buf](https://buf.build/docs/installation) and [protoc](https://grpc.io/docs/protoc-installation/) are installed on your system.

### UV

The project use uv to handle dependencies as well as building the package

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh 
```

### TaskFile

The project use TaskFile to simplify tasks and allow user to seamlessly generate the package with a lot of hidden commands.

```sh
curl -s https://taskfile.dev/install.sh | sh
```
