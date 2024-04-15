import dataclasses


@dataclasses.dataclass
class PackageSpecifier:
    name: bytes
    version: bytes
    release: bytes


def split_name(target: bytes):
    match target.split(b"/", 1):
        case (specifier, _):
            pass
        case (specifier,):
            pass
        case _:
            assert False
    name, version, release = specifier.rsplit(b"-", 2)
    return PackageSpecifier(name=name, version=version, release=release)
