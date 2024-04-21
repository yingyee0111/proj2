from proj.__main__ import (
    main_cmake,
    main_test,
    MainCmakeArgs,
    MainTestArgs,
)
# import subprocess
from pathlib import Path
from proj.config_file import (
    find_config_root, 
    _possible_config_paths,
    get_source_path,
    get_config,
    get_possible_spec_paths,
)
from proj.dtgen.find_outdated import (
    find_outdated,
)

DIR = Path(__file__).absolute().parent

def _test_project(name: str):
    testdir = DIR / name

    cmake_args = MainCmakeArgs(
        path=testdir,
        force=True,
        trace=False,
    )
    main_cmake(args=cmake_args)

    test_args = MainTestArgs(
        path=testdir,
        verbose=False,
        jobs=1,
    )
    main_test(args=test_args)


def test_person():
    _test_project('person')

def test_wrapper():
    _test_project('wrapper')

def test_find_config_root():
    testdir = DIR / 'person'

    assert find_config_root(testdir) == testdir

def test_get_source_path():
    testdir = DIR / 'person'

    correct = testdir / 'src' / 'color.dtg.cc'
    assert get_source_path(testdir / 'include' / 'color.dtg.hh') == correct

def test_get_possible_spec_paths():
    testdir = DIR / 'person'

    found = set(get_possible_spec_paths(testdir / 'include' / 'color.dtg.hh'))
    correct = set([
        testdir / 'include' / 'color.struct.toml',
        testdir / 'include' / 'color.enum.toml',
        testdir / 'include' / 'color.variant.toml',
        testdir / 'src' / 'color.struct.toml',
        testdir / 'src' / 'color.enum.toml',
        testdir / 'src' / 'color.variant.toml',
    ])
    assert found == correct


def test_find_outdated():
    testdir = DIR / 'person'

    config = get_config(testdir)
    
    found = set(find_outdated(testdir, config))
    correct = set([
        testdir / 'include' / 'out_of_date.dtg.hh',
        testdir / 'src' / 'out_of_date2.dtg.cc',
    ])
    assert found == correct
