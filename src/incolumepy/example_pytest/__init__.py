from pathlib import Path
from typing import Tuple
import re
import toml

path = list(Path(__file__).parent.parts)
__path__ = str(Path(*path[:path.index('incolumepy.pytest') + 1]))
__version__ = toml.load(Path(__path__).joinpath('pyproject.toml'))['tool']['poetry']['version']   # '0.1.0'


class VersionError(ValueError):
    pass


def parser_version(s: str) -> Tuple[int, int]:
    # result = tuple(int(x) for x in s.split('.'))
    result = tuple(int(x) for x in re.split(r'[.-]', s))
    if len(result) > 3 or len(result) < 2:
        raise VersionError(f'Expected #.#[.#] bug got {s!r}')
    return result
