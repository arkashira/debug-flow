import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse

@dataclass
class DebugSession:
    code_cells: list
    breakpoint_annotations: list
    variable_snapshots: list

def export_notebook(debug_session: DebugSession) -> str:
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.9.7"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    for code_cell in debug_session.code_cells:
        notebook_cell = {
            "cell_type": "code",
            "execution_count": 0,
            "metadata": {
                "readonly": True
            },
            "outputs": [],
            "source": [code_cell]
        }
        notebook["cells"].append(notebook_cell)

    for annotation in debug_session.breakpoint_annotations:
        notebook_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"Breakpoint: {annotation}"]
        }
        notebook["cells"].append(notebook_cell)

    for snapshot in debug_session.variable_snapshots:
        notebook_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"Variable Snapshot: {snapshot}"]
        }
        notebook["cells"].append(notebook_cell)

    return json.dumps(notebook)

def generate_download_link(notebook: str) -> str:
    expiration_time = datetime.now() + timedelta(hours=24)
    return f"download_notebook?notebook={notebook}&expires={expiration_time.isoformat()}"

def main():
    parser = argparse.ArgumentParser(description="Export debug session as a notebook")
    parser.add_argument("--code-cells", nargs="+", help="Code cells to export")
    parser.add_argument("--breakpoint-annotations", nargs="+", help="Breakpoint annotations to export")
    parser.add_argument("--variable-snapshots", nargs="+", help="Variable snapshots to export")
    args = parser.parse_args()

    debug_session = DebugSession(
        code_cells=args.code_cells,
        breakpoint_annotations=args.breakpoint_annotations,
        variable_snapshots=args.variable_snapshots
    )

    notebook = export_notebook(debug_session)
    download_link = generate_download_link(notebook)

    print(f"Download link: {download_link}")

if __name__ == "__main__":
    main()
