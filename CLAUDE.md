# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `agentic-mesh-protocol` (import name `agentic_mesh_protocol`), a Python package that provides generated gRPC client and server interfaces from Digitalkin's Protocol Buffer definitions. The package is published to PyPI and enables seamless integration with Digitalkin services.

## Architecture

### Code Generation Pipeline

The repository follows a multi-stage generation pipeline:

1. **Proto Source**: Protocol Buffer definitions are maintained in the `agentic-mesh-protocol` git submodule (separate repository)
2. **Code Generation**: Delegates to `amp:generate` (via Taskfile includes), which uses `buf generate` with remote plugins (protocolbuffers/python v33.0 + grpc/python v1.76.0)
3. **File Transfer**: Generated files from `agentic-mesh-protocol/gen/python/` are copied to `src/agentic_mesh_protocol/` and `src/buf/`
4. **Package Building**: Generated code is in `src/agentic_mesh_protocol/` with `__init__.py` files auto-created

### Key Components

- **`agentic-mesh-protocol/` submodule**: Contains upstream `.proto` files and buf configuration for code generation
- **`src/agentic_mesh_protocol/`**: Package root containing all generated code and type stubs
- **`src/buf/`**: Generated protovalidate definitions, importable as `buf.validate`
- **`taskfile.yml`**: Modern task automation with dependency tracking, caching, organized namespaces, and Taskfile includes for delegating proto tasks to the submodule

### Generated Package Structure

After running `task gen`, two top-level packages are shipped, matching the absolute
imports that buf-generated code emits (e.g. `from buf.validate import validate_pb2`):

**`src/agentic_mesh_protocol/`** - one subpackage per service, each versioned under `v1/`:
`cost`, `filesystem`, `gateway`, `module`, `registry`, `setup`, `storage`, `user_profile`.

**`src/buf/validate/`** - protovalidate definitions (generated from buf.build/bufbuild/protovalidate).

Both get `__init__.py` files created automatically for every directory, plus `.pyi` stubs
for type checking.

### What is and is not checked in

Only the hand-maintained skeleton is tracked by git: the `__init__.py` files,
`__version__.py` and `py.typed`. Every `*_pb2.py`, `*_pb2.pyi` and `*_pb2_grpc.py` is
gitignored and rebuilt by `task gen`. **Never edit anything under `src/` by hand** - the
source of truth is `agentic-mesh-protocol/proto/**/*.proto`, and the next generation
overwrites it.

`task gen` wipes `agentic-mesh-protocol/gen/python/` before running buf, because buf only
ever writes files and never removes output for protos that were deleted upstream. Without
the wipe, a removed service leaves an orphaned Python package behind that gets copied into
`src/` forever.

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
4. `task bump-version` only rewrites the version strings; advancing the submodule pointer is a separate step (`git submodule update --remote`)

### Code Generation Details

The `task gen` command performs a 6-step pipeline:

1. **proto:init** - Ensures submodule is initialized
2. **proto:generate** - Wipes `agentic-mesh-protocol/gen/python/`, then delegates to `amp:generate` via Taskfile includes (which executes `npx buf generate` in the submodule with both local proto files AND buf.build/bufbuild/protovalidate module)
3. **proto:copy** - Copies files from `agentic-mesh-protocol/gen/python/` to `src/agentic_mesh_protocol/` and `src/buf/`, guarded by a precondition so an empty generation cannot `rsync --delete` the package away
4. **proto:ensure-init** - Ensures all directories have `__init__.py` files
5. **proto:create-namespaces** - Ensures `src/buf/` and `src/buf/validate/` have `__init__.py` so `from buf.validate import ...` resolves
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

This allows calling submodule tasks directly (e.g., `task amp:generate`, `task amp:lint`, `task amp:format`) while maintaining a clean separation of concerns.

### Testing Generated Code

Tests should import from the public package structure:

```python
from agentic_mesh_protocol.module.v1 import module_service_pb2, module_service_pb2_grpc
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

`[tool.ruff]` in `pyproject.toml` only sets `target-version = "py310"` and
`src = ["src", "test"]`; everything else is Ruff's default (88-char lines, default rule
set). Generated `*_pb2*` files are excluded from mypy via `mypy.ini` and the pre-commit
hook, not from Ruff.

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

**Runtime (included in package)** - pinned exactly, because the generated code is tied to the
protobuf/grpc versions it was built with:

- grpcio==1.82.1, grpcio-tools==1.82.1
- protobuf==7.35.1
- googleapis-common-protos==1.75.0
- protovalidate==1.2.0 (runtime validation library)
- bump-my-version>=1.4.1

**Development group (via [dependency-groups], PEP 735):**

- `dev`: pytest, ruff, mypy, pre-commit, build, twine, bump-my-version

Install with: `uv sync` (installs runtime + dev group by default)

## Package Metadata

- **Distribution name**: `agentic-mesh-protocol` / **import name**: `agentic_mesh_protocol`
- **Current version**: 1.0.1 (tracked in `pyproject.toml`, `.bumpversion.toml` and `src/agentic_mesh_protocol/__version__.py`)
- **License**: Proprietary
- **Python support**: classifiers advertise 3.10-3.14; the CI matrix tests 3.10-3.13
- **Build system**: setuptools with modern pyproject.toml (PEP 517/518)
- **Dependency management**: uv with dependency-groups (PEP 735)
