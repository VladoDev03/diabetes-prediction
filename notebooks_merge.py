import nbformat
from pathlib import Path

def merge_notebooks(notebook_paths, output_path):
    """
    Merges multiple .ipynb files into one, in the given order,
    inserting a markdown separator before each source notebook's cells.
    """
    merged = nbformat.v4.new_notebook()
    merged.cells = []

    for path in notebook_paths:
        nb = nbformat.read(path, as_version=4)

        separator = nbformat.v4.new_markdown_cell(f"<!-- === From: {path} === -->")
        merged.cells.append(separator)
        merged.cells.extend(nb.cells)

    nbformat.write(merged, output_path)
    print(f"Merged {len(notebook_paths)} notebooks into {output_path}")


# Correct notebook order based
notebook_order = [
    "notebooks/brfss/01_cleanup.ipynb",
    "notebooks/diabetes/01_EDA.ipynb",
    "notebooks/brfss/02_EDA.ipynb",
    "notebooks/diabetes/02_preprocessing.ipynb",
    "notebooks/brfss/03_preprocessing.ipynb",
    "notebooks/diabetes/03_train.ipynb",
    "notebooks/brfss/04_train.ipynb"
]

merge_notebooks(notebook_order, "final_project.ipynb")
