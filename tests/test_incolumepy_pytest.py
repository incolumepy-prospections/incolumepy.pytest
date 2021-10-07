import pytest
import re
from src.incolumepy.example_pytest import __version__, parser_version, VersionError


def test_version():
    # assert __version__ == "0.1.0"
    assert re.fullmatch(r'\d.\d.\d(-.*.?\d)?', __version__, flags=re.I)


@pytest.mark.parametrize(
    ("strinput", "expected"),
    (
        ("2.7", (2, 7)),
        ("3.9", (3, 9)),
        ("3.10", (3, 10)),
    ),
)
def test_parser_version_minors(strinput, expected):
    assert parser_version(strinput) == expected


@pytest.mark.parametrize(
    ("strinput", "expected"),
    (
        ("2.7.6", (2, 7, 6)),
        ("3.8.16", (3, 8, 16)),
        ("3.9.7", (3, 9, 7)),
        ("3.10.1", (3, 10, 1)),
    ),
)
def test_parser_version_patches(strinput, expected):
    assert parser_version(strinput) == expected


def test_parser_version_not_number():
    with pytest.raises(ValueError):
        parser_version('3.n')


@pytest.mark.parametrize(
    ("strinput", "expected"),
    (
        ('3', 'Expected #.#[.#] bug got "3"'),
        ('3.1.1.1', 'Expected #.#[.#] bug got "3.1.1.1"'),
    )
)
def test_parser_version_failure_segment_count(strinput, expected):
    with pytest.raises(VersionError) as e:
        parser_version(strinput)
    msg, = e.value.args
    assert msg == f'Expected #.#[.#] bug got {strinput!r}'


@pytest.mark.parametrize(
    ("strinput", "expected"),
    (
        ('3.1.0-dev0', f"invalid literal for int() with base 10: 'dev0'"),
        ('3.1.1-dev.0', f"invalid literal for int() with base 10: 'dev'"),
        ('3.10.0-alpha.0', f"invalid literal for int() with base 10: 'alpha'"),
        ('3.11.0-a.1', f"invalid literal for int() with base 10: 'a'"),
        ('3.11.0.a.2', f"invalid literal for int() with base 10: 'a'"),
    )
)
def test_parser_version_failure_segment_unstable(strinput, expected):
    with pytest.raises(ValueError) as e:
        parser_version(strinput)
    msg, = e.value.args
    assert msg == expected

