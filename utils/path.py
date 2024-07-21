def relative_from_root(path: str):
    from pathlib import Path
    return Path(__file__).parent.parent.joinpath(path).absolute().__str__()