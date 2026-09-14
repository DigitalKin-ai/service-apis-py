# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `agentic-mesh-protocol` (import name `agentic_mesh_protocol`), a Python package that provides generated gRPC client and server interfaces from Digitalkin's Protocol Buffer definitions. The package is published to PyPI and enables seamless integration with Digitalkin services.

## Architecture

### Code Generation Pipeline

The repository follows a multi-stage generation pipeline:

1. **Proto Source**: Protocol Buffer definitions are maintained in the `agentic-mesh-protocol` git submodule (separate repository)
2. **Code Generation**: Runs `buf generate --template buf.gen.yaml` inside the submodule, with remote plugins (protocolbuffers/python v33.0 + grpc/python v1.76.0). Uses `buf` from `PATH`, falling back to the submodule's `npx --no-install buf`
3. **File Transfer**: `gen/` is wiped and replaced by `agentic-mesh-protocol/gen/python/`
4. **Scaffolding**: `__init__.py` in every directory, `__version__.py` (version read from `pyproject.toml`) and `py.typed` are generated too

### Key Components

- **`agentic-mesh-protocol/` submodule**: Contains upstream `.proto` files and buf configuration for code generation
- **`gen/`**: Package root (`package-dir = { "" = "gen" }` in `pyproject.toml`), 100% generated and gitignored
- **`gen/agentic_mesh_protocol/`**: All generated code and type stubs
- **`gen/buf/`**: Generated protovalidate definitions, importable as `buf.validate`
- **`taskfile.yml`**: Task automation with dependency tracking and caching; the submodule's own Taskfile is included as `amp:*`

### Generated Package Structure

After running `task gen`, two top-level packages are shipped, matching the absolute
imports that buf-generated code emits (e.g. `from buf.validate import validate_pb2`):

**`gen/agentic_mesh_protocol/`** - one subpackage per proto package, each versioned under `v1/`:
`common`, `cost`, `filesystem`, `gateway`, `module`, `pagination`, `registry`, `setup`,
`storage`, `user_profile`.

**`gen/buf/validate/`** - protovalidate definitions (generated from buf.build/bufbuild/protovalidate).

Both get `__init__.py` files created automatically for every directory, plus `.pyi` stubs
for type checking.

### What is and is not checked in

Nothing importable is tracked by git: the whole `gen/` directory, including `__init__.py`,
`__version__.py` and `py.typed`, is rebuilt by `task gen` (see the `proto:scaffold` task
to change those files). **Never edit anything under `gen/` by hand** - the source of truth
is `agentic-mesh-protocol/proto/**/*.proto`, and the next generation overwrites it.

`task gen` wipes `agentic-mesh-protocol/gen/python/` before running buf, because buf only
ever writes files and never removes output for protos that were deleted upstream. Without
the wipe, a removed service leaves an orphaned Python package behind that gets copied into
`gen/` forever.

`task gen` is cached on the protos, the buf config and `pyproject.toml`; use
`task gen --force` to regenerate anyway. `task test` and `task build` depend on it.

Taskfile gotcha: vars of the included submodule Taskfile are global, so a root var named
like one of them (e.g. `GEN_DIR`) is silently overridden - hence `GEN_ROOT`.

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

The `task gen` command performs a 4-step pipeline:

1. **proto:init** - Ensures submodule is initialized
2. **proto:generate** - Wipes `agentic-mesh-protocol/gen/python/`, then runs `buf generate --template buf.gen.yaml` in the submodule (local proto files AND the buf.build/bufbuild/protovalidate module)
3. **proto:copy** - Replaces `gen/` with `agentic-mesh-protocol/gen/python/`, guarded by preconditions so an empty generation cannot wipe the package away
4. **proto:scaffold** - Writes `gen/agentic_mesh_protocol/__init__.py` (exposes `__version__`), `__version__.py` and `py.typed`, and adds an empty `__init__.py` to every other directory so `from buf.validate import ...` resolves

Building is separate: `task build` depends on `task gen` and writes to `dist/`.

### Taskfile Includes Pattern

The submodule's Taskfile is included (optional, overridable with `AMP_DIR`):

```yaml
includes:
  amp:
    taskfile: '{{.AMP_DIR | default "agentic-mesh-protocol"}}/Taskfile.yml'
    dir: '{{.AMP_DIR | default "agentic-mesh-protocol"}}'
    optional: true
```

This exposes submodule tasks directly (e.g. `task amp:gen`, `task amp:lint`, `task amp:version:breaking`).
They use `npx buf` and therefore need `task amp:install`; the root `proto:*` tasks call buf
directly instead, so CI needs no Node setup.

### Testing Generated Code

Tests should import from the public package structure:

```python
from agentic_mesh_protocol.module.v1 import module_service_pb2, module_service_pb2_grpc
```

### CI/CD Pipeline

- CI runs on pushes to `dev` and PRs to `main`/`dev`
- Tests across Python 3.10, 3.11, 3.12, 3.13
- Workflow: submodule checkout → `task gen` → `uv sync --locked` → `task lint` → `task test` → `task build`
- Use `task ci` to run the full CI pipeline locally
- Use `task ci:quick` for faster feedback (lint only)
- Publishing: creating a GitHub Release runs `publish.yml` (gen → test → build `dist/` → TestPyPI → PyPI);
  the version is whatever `pyproject.toml` says, so bump it before tagging

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
- **Proto**: `gen`, `proto:*` namespace (init, generate, copy, scaffold, clean, lint, format, format:check, breaking)
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
`src = ["gen", "test"]`; everything else is Ruff's default (88-char lines, default rule
set). Ruff skips `gen/` because it is gitignored; it does format Python blocks in
`README.md`. `gen/` is also excluded from mypy via `mypy.ini` and the pre-commit hook.

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
- buf (`brew install bufbuild/buf/buf`; CI uses `bufbuild/buf-action`). Without it on `PATH`,
  `task install:amp` installs the submodule's npm copy, which the taskfile falls back to

### Python Dependencies

**Runtime (included in package)** - pinned exactly, because the generated code is tied to the
protobuf/grpc versions it was built with:

- grpcio==1.83.1, grpcio-tools==1.83.1
- protobuf==7.36.0
- googleapis-common-protos==1.75.2
- protovalidate==1.2.0 (runtime validation library)
- bump-my-version>=1.5.1

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
