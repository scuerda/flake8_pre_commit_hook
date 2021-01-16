import argparse
import subprocess
import sys

from pathlib import Path
from typing import Optional
from typing import Sequence
from collections import defaultdict


def run_flake8(working_dir, files):
    res = subprocess.run(('flake8', " ".join(files)), cwd=working_dir)
    return res.returncode


def walk_up_to_flake(starting_dir: Path) -> str:
    if '.flake8' in [f.name for f in starting_dir.iterdir() if f.is_file]:
        return starting_dir.absolute().as_posix()
    else:
        return walk_up_to_flake(starting_dir.parent)


def find_dirs_to_run_flake(files: list) -> list:
    flake_map = defaultdict(list)
    for f in files:
        if not f.endswith('.py'):
            continue
        file_path = Path(f)
        starting_dir = file_path.parent
        flake_dir = walk_up_to_flake(starting_dir)
        flake_map[flake_dir].append(file_path.absolute().as_posix())

    return flake_map


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files',
        nargs='*',
        help='Provide paths and targets for running flake8',
    )
    args = parser.parse_args(argv)
    flake_map = find_dirs_to_run_flake(args.files)
    results = []
    for working_dir, files in flake_map.items():
        flake_output = run_flake8(working_dir, files)
        if flake_output == 1:
            results.append((working_dir, 1))
    if results:
        sys.exit(1)
    return sys.exit(0)
