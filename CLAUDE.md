# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `digitalkin_proto`, a Python package that provides generated gRPC client and server interfaces from Digitalkin's Protocol Buffer definitions. The package is published to PyPI and enables seamless integration with Digitalkin services.

## Architecture

### Code Generation Pipeline

The repository follows a multi-stage generation pipeline:

1. **Proto Source**: Protocol Buffer definitions are maintained in the `agentic-mesh-protocol` git submodule (separate repository)
2. **Code Generation**: Delegates to `amp:generate:python` (via Taskfile includes), which uses `buf generate` with remote plugins (protocolbuffers/python v33.0 + grpc/python v1.76.0)
3. **File Transfer**: Generated files from `agentic-mesh-protocol/gen/python/` are copied to `src/digitalkin_proto/`
4. **Package Building**: Generated code is in `src/digitalkin_proto/` with `__init__.py` files auto-created

### Key Components

- **`agentic-mesh-protocol/` submodule**: Contains upstream `.proto` files and buf configuration for code generation
- **`src/digitalkin_proto/`**: Package root containing all generated code and type stubs
- **`taskfile.yml`**: Modern task automation with dependency tracking, caching, organized namespaces, and Taskfile includes for delegating proto tasks to the submodule

### Generated Package Structure

After running `task gen`, the package contains:

**Primary package** (`src/digitalkin_proto/`):

- `agentic_mesh_protocol/*/v1/` - Versioned service implementations (module, module_registry, storage, filesystem, cost, setup, user_profile)
- `buf/validate/` - Protocol buffer validation definitions (generated from buf.build/bufbuild/protovalidate)
- `__init__.py` files created automatically for all directories
- `.pyi` stub files for type checking

**Top-level namespace packages** (for import compatibility):

- `src/buf/` - Copy of `digitalkin_proto.buf` to support `from buf.validate import` statements in generated code
- `src/agentic_mesh_protocol/` - Copy of `digitalkin_proto.agentic_mesh_protocol` to support cross-module imports in generated code

These namespace packages are necessary because buf-generated Python code uses absolute imports (e.g., `from buf.validate import validate_pb2`) rather than relative imports. The `proto:create-namespaces` task automatically creates these during generation.

## Common Development Commands

### Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Complete setup (submodules + deps + hooks)
task setup

# Or run individual steps:
task init      # Initialize submodules
task install   # Install dependencies (alias: deps, sync)
```

### Development Workflow

```bash
# Start fresh development environment
task dev       # Runs: setup + generate proto + ready message

# Validate your setup
task validate  # Check all required tools are installed

# Quick health check
task check     # Validate + quick lint + confirmation
```

### Code Generation

```bash
# Generate Python code from proto files
task gen       # Aliases: generate, gen-proto, proto

# Get detailed info about generation process
task gen --summary

# Clean generated files
task proto:clean
```

### Proto Quality (Delegated to Submodule)

```bash
# Lint proto files
task proto:lint

# Format proto files
task proto:format

# Check proto formatting
task proto:format:check

# Check for breaking changes
task proto:breaking
```

### Code Quality

```bash
# Format code
task fmt       # Alias: format

# Fix all issues (format + lint)
task lint:fix  # Alias: fix

# Check code quality (format + lint + types)
task lint

# Run pre-commit hooks
task pre-commit
```

### Testing

```bash
# Run tests
task test      # Alias: t
task test -- -v -k test_name  # Pass args to pytest

# Watch mode (requires pytest-watch)
task test:watch
```

### Building and Publishing

```bash
# Build package
task build

# Publish to TestPyPI
task publish:test  # Alias: publish-test

# Publish to PyPI
task publish:prod  # Aliases: publish, release
```

### Version Management

```bash
# Bump version
task bump-version -- patch   # Default: patch (0.1.16 → 0.1.17)
task bump-version -- minor   # 0.1.16 → 0.2.0
task bump-version -- major   # 0.1.16 → 1.0.0
task bump-version -- pre_l   # Pre-release label (alpha, beta, rc)
task bump-version -- pre_n   # Pre-release number
```

### CI/CD

```bash
# Run full CI pipeline locally
task ci        # Lint + test + build

# Quick CI checks
task ci:quick  # Format check + lint only
```

### Cleanup

```bash
# Remove build artifacts and cache
task clean

# Deep clean (generated code + venv + all artifacts)
task clean:full  # Aliases: clean-all, reset
```

### Utilities

```bash
# List all available tasks
task --list
task           # Default task shows list
```

## Important Workflow Details

### Modifying Proto Definitions

1. Proto files live in the `agentic-mesh-protocol` submodule, NOT in this repository
2. To update protos: modify them in the `agentic-mesh-protocol` repository, then update the submodule reference here
3. After updating submodule: run `task gen-proto` to regenerate Python code
4. The `bump-version` task automatically pulls latest from submodule's dev branch

### Code Generation Details

The `task gen` command performs a 6-step pipeline:

1. **proto:init** - Ensures submodule is initialized
2. **proto:generate** - Delegates to `amp:generate` via Taskfile includes (which executes `npx buf generate` in the submodule with both local proto files AND buf.build/bufbuild/protovalidate module)
3. **proto:copy** - Copies files from `agentic-mesh-protocol/gen/python/` to `src/digitalkin_proto/`
4. **proto:ensure-init** - Ensures all directories have `__init__.py` files
5. **proto:create-namespaces** - Creates top-level `buf/` and `agentic_mesh_protocol/` namespace packages for import compatibility
6. **build** - Builds the Python package

The pipeline uses Task's `sources`/`generates` for intelligent caching - steps are skipped if inputs haven't changed.

### Taskfile Includes Pattern

The main taskfile uses Taskfile's `includes` feature to delegate proto-related operations to the submodule:

```yaml
includes:
  amp:
    taskfile: ./agentic-mesh-protocol/Taskfile.yml
    dir: ./agentic-mesh-protocol
```

This allows calling submodule tasks directly (e.g., `task amp:generate:python`, `task amp:lint`, `task amp:format`) while maintaining a clean separation of concerns.

### Testing Generated Code

Tests should import from the public package structure:

```python
from digitalkin_proto.agentic_mesh_protocol.module.v1 import module_pb2, module_service_pb2_grpc
```

### CI/CD Pipeline

- CI runs on pushes to `dev` and PRs to `main`/`dev`
- Tests across Python 3.10, 3.11, 3.12, 3.13
- Workflow: submodule checkout → buf generate (via submodule) → lint → test → build
- Use `task ci` to run the full CI pipeline locally
- Use `task ci:quick` for faster feedback (lint only)
- Publishing to PyPI happens via GitHub Release workflow (automated version bump + publish)

## Taskfile Features

The modernized `taskfile.yml` includes:

### Task Organization

- **Includes**: Delegates proto-related tasks to the submodule using `amp:*` namespace
- **Namespaced tasks**: Related tasks grouped with `:` separator (e.g., `proto:init`, `lint:fix`, `version:bump`)
- **Aliases**: Common shortcuts (e.g., `task t` for `task test`, `task fmt` for `task format`)
- **Internal tasks**: Implementation details marked as `internal: true` (hidden from `task --list`)
- **Default task**: Running just `task` shows the task list

### Smart Execution

- **Dependency tracking**: Uses `sources`/`generates` to skip unchanged work
- **Preconditions**: Tasks validate requirements before running
- **Status checks**: Tasks skip if already completed (e.g., submodule already initialized)
- **Deps**: Tasks can depend on other tasks running first

### Developer Experience

- **Summaries**: Extended help with `--summary` flag
- **CLI args**: Pass arguments through with `{{.CLI_ARGS}}`
- **Variables**: Centralized configuration in `vars` section
- **Dotenv support**: Automatically loads `.env` file if present

### Key Task Categories

- **Setup**: `init`, `install`, `setup`, `dev`, `install:hooks`
- **Proto**: `gen`, `proto:*` namespace (init, generate, copy, ensure-init, clean, lint, format, format:check, breaking)
- **Quality**: `fmt`, `lint`, `lint:*`, `pre-commit`
- **Testing**: `test`, `test:watch`
- **Build/Publish**: `build`, `publish:test`, `publish:prod`
- **Version**: `bump-version`
- **CI**: `ci`, `ci:quick`, `check`
- **Cleanup**: `clean`, `clean:full`
- **Utils**: `validate`

## Code Quality Standards

### Ruff Configuration

- Line length: 100 characters
- Enabled rules: pycodestyle, pyflakes, isort, pydocstyle (Google convention), pyupgrade, naming, bugbear, comprehensions, simplify
- Format: double quotes, space indentation
- Known first-party: `digitalkin_proto`

### Pre-commit Hooks

- Trailing whitespace removal
- End-of-file fixer
- YAML/TOML validation
- Ruff formatting and linting
- MyPy type checking

## Dependencies

### Required Tools

- Python 3.10+
- uv (package manager and project manager)
- Task (task runner)
- rsync (for copying generated files)

Note: `buf` and `protoc` are handled by the submodule via npx, no local installation needed

### Python Dependencies

**Runtime (included in package):**

- grpcio>=1.76.0, grpcio-tools>=1.76.0
- protobuf>=6.33.0
- googleapis-common-protos>=1.71.0
- protovalidate>=1.0.0 (runtime validation library)
- bump-my-version>=1.2.4

**Development groups (via [dependency-groups], PEP 735):**

- `dev`: All development dependencies (pytest, ruff, mypy, pre-commit, build tools)
- `test`: pytest
- `lint`: ruff, pre-commit
- `build`: build, twine, bump2version

Install with: `uv sync` (installs runtime + dev group by default)

## Package Metadata

- **Package name**: `digitalkin_proto`
- **Current version**: 0.1.16 (tracked in `pyproject.toml` and `src/digitalkin_proto/__init__.py`)
- **License**: Proprietary
- **Python support**: 3.10, 3.11, 3.12, 3.13
- **Build system**: setuptools with modern pyproject.toml (PEP 517/518)
- **Dependency management**: uv with dependency-groups (PEP 735)
