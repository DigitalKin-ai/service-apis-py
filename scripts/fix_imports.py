"""This script fixes imports in all Python files in the specified directory."""

import re
from pathlib import Path


def fix_imports(directory):
    """Fix imports in all Python files in the specified directory."""
    for path in Path(directory).rglob("*.py*"):  # Match .py and .pyi files
        if path.is_file():
            print(f"Processing file: {path}")
            try:
                with open(path, "r", encoding="utf-8") as f:  # noqa: UP015
                    content = f.read()

                # Fix imports for from ... import ...
                content = re.sub(r"from\s+(digitalkin)\.", r"from digitalkin_proto.\1.", content)

                # Fix imports for import ...
                content = re.sub(
                    r"import\s+(digitalkin)\.", r"import digitalkin_proto.\1.", content
                )

                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed imports in {path}")
            except UnicodeDecodeError:
                print(f"Warning: Skipping file {path} - not a UTF-8 text file")
            except Exception as e:
                print(f"Error processing {path}: {e}")


if __name__ == "__main__":
    fix_imports("src/digitalkin_proto")
