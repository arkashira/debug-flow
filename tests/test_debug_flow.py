import pytest
from debug_flow import DebugSession, export_notebook, generate_download_link

def test_export_notebook():
    debug_session = DebugSession(
        code_cells=["print('Hello World')"],
        breakpoint_annotations=["Breakpoint 1"],
        variable_snapshots=["Variable 1 = 10"]
    )

    notebook = export_notebook(debug_session)
    assert "cells" in notebook
    assert "metadata" in notebook

def test_generate_download_link():
    notebook = '{"cells": [], "metadata": {}}'
    download_link = generate_download_link(notebook)
    assert "download_notebook?" in download_link
    assert "expires" in download_link

def test_main():
    # Test with valid arguments
    import sys
    sys.argv = ["debug_flow.py", "--code-cells", "print('Hello World')", "--breakpoint-annotations", "Breakpoint 1", "--variable-snapshots", "Variable 1 = 10"]
    from debug_flow import main
    main()

    # Test with invalid arguments
    sys.argv = ["debug_flow.py", "--invalid-arg"]
    with pytest.raises(SystemExit):
        main()
