#!/usr/bin/env python

"""Tests for `flake8_pre_commit_hook` package."""

import pytest
from typing import List
from pathlib import Path

from flake8_pre_commit_hook.flake8_pre_commit_hook import find_dirs_to_run_flake


def make_tmp_files(tmp_path, files) -> List[str]:
    full_paths = []
    full_tmp_path = tmp_path
    for f in files:
        if '/' in f:
            parts = f.split('/')
            f = parts[-1]
            full_tmp_path = tmp_path
            for sub_dir in parts[:-1]:
                full_tmp_path = full_tmp_path / sub_dir
                if not full_tmp_path.exists():
                    full_tmp_path.mkdir()
        p = full_tmp_path / f
        p.touch()
        full_paths.append(str(p))
    return full_paths


@pytest.fixture
def in_same_dir(tmp_path):
    staged_files = ['.flake8', 'test.py']
    return make_tmp_files(tmp_path, staged_files)


@pytest.fixture
def with_sub_dir(tmp_path):
    staged_files = ['.flake8', 'test.py', 'subdir/test2.py']
    return make_tmp_files(tmp_path, staged_files)


@pytest.fixture
def with_flake8_in_subdir(tmp_path):
    staged_files = ['.flake8', 'test.py', 'subdir/.flake8', 'subdir/test2.py']
    return make_tmp_files(tmp_path, staged_files)


def test_same_dir(in_same_dir, tmp_path):
    assert tmp_path.as_posix() in find_dirs_to_run_flake(in_same_dir)


def test_with_sub_dir(with_sub_dir, tmp_path):
    expected = [f for f in with_sub_dir if f.endswith('.py')]
    flake8_map = find_dirs_to_run_flake(with_sub_dir)
    assert tmp_path.as_posix() in flake8_map
    assert flake8_map[tmp_path.as_posix()] == expected


def test_with_two_flake_files(with_flake8_in_subdir, tmp_path):
    flake8_map = find_dirs_to_run_flake(with_flake8_in_subdir)
    assert [Path(f).name for f in flake8_map[tmp_path.as_posix()]] == ['test.py']
    other_key = tmp_path.joinpath('subdir').as_posix()
    assert [Path(f).name for f in flake8_map[other_key]] == ['test2.py']
    

