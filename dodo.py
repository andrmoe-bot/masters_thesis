import os
from typing import Generator
from doit.tools import create_folder


def get_file_refs(file_path: str) -> Generator[str, None, None]:
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    with open(file_path, "r") as f:
        file_content = f.read()
        for file in files:
            ext = file.split(".")[-1]
            file_no_ext = file.replace("."+ext, "")
            if (
                file in file_content
                or "{" + file_no_ext in file_content
                or f"import {file_no_ext}" in file_content
                or f"from {file_no_ext}" in file_content
            ):
                yield file


def task_temp_folder():
    return {'actions': [(create_folder, ['temp'])], 'targets': ['temp']}


def task_compile_pdf():
    report_name = "autoreproduce"
    return {
        "actions": [
            [
                "latexmk",
                "-f",
                "-pdf",
                "-interaction=nonstopmode",
                f"{report_name}.tex",
            ]
        ],
        "file_dep": ["refs.bib", f"{report_name}.tex"],
        "targets": [f"{report_name}.pdf"],
    }
