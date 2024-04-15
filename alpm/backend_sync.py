import dataclasses
import itertools
import tarfile
from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar

import alpm.dependency
import alpm.package
import alpm.util

T = TypeVar("T")


@dataclasses.dataclass
class Item(Generic[T]):
    value: T


@dataclasses.dataclass
class Name(Item[bytes]):
    pass


@dataclasses.dataclass
class Version(Item[bytes]):
    pass


@dataclasses.dataclass
class Filename(Item[bytes]):
    pass


@dataclasses.dataclass
class Base(Item[bytes]):
    pass


@dataclasses.dataclass
class Description(Item[bytes]):
    pass


@dataclasses.dataclass
class URL(Item[bytes]):
    pass


@dataclasses.dataclass
class Architecture(Item[bytes]):
    pass


@dataclasses.dataclass
class Packager(Item[bytes]):
    pass


@dataclasses.dataclass
class MD5SUM(Item[bytes]):
    pass


@dataclasses.dataclass
class SHA256SUM(Item[bytes]):
    pass


@dataclasses.dataclass
class Signature(Item[bytes]):
    pass


@dataclasses.dataclass
class BuildDate(Item[bytes]):
    pass


@dataclasses.dataclass
class CompressedSize(Item[bytes]):
    pass


@dataclasses.dataclass
class InstalledSize(Item[bytes]):
    pass


@dataclasses.dataclass
class List(Generic[T]):
    values: tuple[T, ...]


@dataclasses.dataclass
class Groups(List[bytes]):
    pass


@dataclasses.dataclass
class License(List[bytes]):
    pass


@dataclasses.dataclass
class Replaces(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class Depends(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class OptionalDepends(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class MakeDepends(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class CheckDepends(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class Conflicts(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class Provides(List[alpm.dependency.Dependency]):
    pass


@dataclasses.dataclass
class Files(List[bytes]):
    pass


@dataclasses.dataclass
class ExtendedData(List[tuple[bytes, bytes]]):
    pass


def remove_suffix(s: bytes, suffix: bytes):
    if s.endswith(suffix):
        s = s[: -len(suffix)]
    else:
        suffix = b""
    return s, suffix


def parse_list(lines: Iterator[bytes]):
    for line in lines:
        value, suffix = remove_suffix(line, b"\n")
        if value:
            yield value
        else:
            yield suffix
            break
    else:
        yield b""


def is_space(c: int):
    return c in b"\f\n\r\t\v"


def is_digit(c: int):
    return c in b"0123456789"


class Error(Exception):
    pass


def assert_all_digits(line: Iterator[int]):
    c = next(line)
    if not is_digit(c):
        raise Error
    if not all(is_digit(c) for c in line):
        raise Error


def parse_date(line: bytes):
    iterator = iter(line)
    c = next(iterator)
    while is_space(c):
        c = next(iterator)
    if c in b"+-":
        c = next(iterator)
    assert_all_digits(itertools.chain((c,), iterator))
    return line


def parse_dependency(lines: Iterator[bytes]):
    *values, suffix = parse_list(lines)
    return (alpm.dependency.dependency_from_string(value) for value in values), suffix


def no_x00(s: Iterable[bytes]):
    for line in s:
        assert b"\x00" not in line
        yield line


def scan(lines: Iterator[bytes]):
    item_classes = dict[
        bytes,
        type[
            Name
            | Version
            | Filename
            | Base
            | Description
            | URL
            | Architecture
            | Packager
            | MD5SUM
            | SHA256SUM
            | Signature
        ],
    ](
        {
            b"%NAME%": Name,
            b"%VERSION%": Version,
            b"%FILENAME%": Filename,
            b"%BASE%": Base,
            b"%DESC%": Description,
            b"%URL%": URL,
            b"%ARCH%": Architecture,
            b"%PACKAGER%": Packager,
            b"%MD5SUM%": MD5SUM,
            b"%SHA256SUM%": SHA256SUM,
            b"%PGPSIG%": Signature,
        }
    )
    bytes_classes = dict[bytes, type[Groups | License | Files]](
        {b"%GROUPS%": Groups, b"%LICENSE%": License, b"%FILES%": Files}
    )
    size_classes = dict[bytes, type[CompressedSize | InstalledSize]](
        {b"%CSIZE%": CompressedSize, b"%ISIZE%": InstalledSize}
    )
    dependency_class = dict[
        bytes,
        type[
            Replaces
            | Depends
            | OptionalDepends
            | MakeDepends
            | CheckDepends
            | Conflicts
            | Provides
        ],
    ](
        {
            b"%REPLACES%": Replaces,
            b"%DEPENDS%": Depends,
            b"%OPTDEPENDS%": OptionalDepends,
            b"%MAKEDEPENDS%": MakeDepends,
            b"%CHECKDEPENDS%": CheckDepends,
            b"%CONFLICTS%": Conflicts,
            b"%PROVIDES%": Provides,
        }
    )
    for line in lines:
        match line.removesuffix(b"\n"):
            case b"%NAME%" | b"%VERSION%" | b"%FILENAME%" | b"%BASE%" | b"%DESC%" | b"%URL%" | b"%ARCH%" | b"%PACKAGER%" | b"%MD5SUM%" | b"%SHA256SUM%" | b"%PGPSIG%" as key:
                value, suffix = remove_suffix(next(lines), b"\n")
                yield item_classes[key](value=value)
            case b"%GROUPS%" | b"%LICENSE%" | b"%FILES%" as key:
                *values, suffix = parse_list(lines)
                yield bytes_classes[key](values=tuple(values))
            case b"%BUILDDATE%":
                value, suffix = remove_suffix(next(lines), b"\n")
                yield BuildDate(parse_date(value))
            case b"%CSIZE%" | b"%ISIZE%" as key:
                value, suffix = remove_suffix(next(lines), b"\n")
                assert_all_digits(iter(value))
                yield size_classes[key](value=value)
            case b"%REPLACES%" | b"%DEPENDS%" | b"%OPTDEPENDS%" | b"%MAKEDEPENDS%" | b"%CHECKDEPENDS%" | b"%CONFLICTS%" | b"%PROVIDES%" as key:
                values, suffix = parse_dependency(lines)
                yield dependency_class[key](values=tuple(values))
            case b"%DATA%":
                *values, suffix = parse_list(lines)
                yield ExtendedData(
                    values=tuple(
                        alpm.package.parse_extended_data(value) for value in values
                    )
                )
            case _:
                if line != b"\n":
                    assert False
                yield line
                continue
        yield suffix


@dataclasses.dataclass
class Package:
    filename: bytes | None
    base: bytes | None
    name: bytes
    version: bytes
    release: bytes
    description: bytes | None
    url: bytes | None
    packager: bytes | None
    md5sum: bytes | None
    sha256sum: bytes | None
    base64_signature: bytes | None
    architecture: bytes | None
    build_date: int | None

    compressed_size: int | None
    installed_size: int | None

    licenses: list[bytes]
    replaces: list[alpm.dependency.Dependency]
    groups: list[bytes]
    depends: list[alpm.dependency.Dependency]
    optional_depends: list[alpm.dependency.Dependency]
    check_depends: list[alpm.dependency.Dependency]
    make_depends: list[alpm.dependency.Dependency]
    conflicts: list[alpm.dependency.Dependency]
    provides: list[alpm.dependency.Dependency]

    files: tuple[bytes, ...] | None

    extended_data: list[tuple[bytes, bytes]]


def empty_package(name: bytes, version: bytes, release: bytes):
    return Package(
        filename=None,
        base=None,
        name=name,
        version=version,
        release=release,
        description=None,
        url=None,
        packager=None,
        md5sum=None,
        sha256sum=None,
        base64_signature=None,
        architecture=None,
        build_date=None,
        compressed_size=None,
        installed_size=None,
        licenses=[],
        replaces=[],
        groups=[],
        depends=[],
        optional_depends=[],
        check_depends=[],
        make_depends=[],
        conflicts=[],
        provides=[],
        files=None,
        extended_data=[],
    )


def validate_filename(value: bytes):
    if value.startswith(b"."):
        raise Error
    elif b"/" in value:
        raise Error
    elif len(value) > 4096:
        raise Error


def validate_int64(value: bytes):
    result = int(value, base=10)
    if not -9223372036854775808 <= result <= 9223372036854775807:
        raise Error
    return result


def to_package(
    package: Package,
    tokens: Iterable[
        Name
        | Version
        | Filename
        | Base
        | Description
        | URL
        | Architecture
        | Packager
        | MD5SUM
        | SHA256SUM
        | Signature
        | Groups
        | License
        | BuildDate
        | CompressedSize
        | InstalledSize
        | Replaces
        | Depends
        | OptionalDepends
        | MakeDepends
        | CheckDepends
        | Conflicts
        | Provides
        | Files
        | ExtendedData
        | bytes
    ],
):
    for token in tokens:
        match token:
            case Name(value):
                if package.name != value:
                    raise Error
            case Version(value):
                version, release = value.split(b"-", 1)
                if package.version != version or package.release != release:
                    raise Error
            case Filename(value):
                validate_filename(value)
                package.filename = value
            case Base(value):
                package.base = value
            case Description(value):
                package.description = value
            case URL(value):
                package.url = value
            case Architecture(value):
                package.architecture = value
            case Packager(value):
                package.packager = value
            case MD5SUM(value):
                package.md5sum = value
            case SHA256SUM(value):
                package.sha256sum = value
            case Signature(value):
                package.base64_signature = value
            case Groups(values):
                package.groups += values
            case License(values):
                package.licenses += values
            case BuildDate(value):
                package.build_date = validate_int64(value)
            case CompressedSize(value):
                package.compressed_size = validate_int64(value)
            case InstalledSize(value):
                package.installed_size = validate_int64(value)
            case Replaces(values):
                package.replaces += values
            case Depends(values):
                package.depends += values
            case OptionalDepends(values):
                package.optional_depends += values
            case MakeDepends(values):
                package.make_depends += values
            case CheckDepends(values):
                package.check_depends += values
            case Conflicts(values):
                package.conflicts += values
            case Provides(values):
                package.provides += values
            case Files(values):
                package.files = values
            case ExtendedData(values):
                package.extended_data += values
            case bytes():
                pass
            case _:
                assert False


def entry_filename(name: bytes):
    split = name.rsplit(b"/", 1)
    try:
        _, filename = split
    except ValueError:
        filename = None
    return filename


def sync_db_read(package: Package, lines: Iterator[bytes]):
    to_package(package, scan(no_x00(lines)))


def tar_file_to_packages(db: dict[bytes, Package], tar_file: tarfile.TarFile):
    for info in tar_file:
        if info.isdir():
            continue
        assert not info.issparse()
        name = info.name.encode()
        filename = entry_filename(name)
        if filename not in (b"desc", b"depends", b"files"):
            assert False
        package_specifier = alpm.util.split_name(name)
        try:
            package = db[package_specifier.name]
        except KeyError:
            package = empty_package(
                name=package_specifier.name,
                version=package_specifier.version,
                release=package_specifier.release,
            )
            db[package_specifier.name] = package
        # file = tar_file.extractfile(info)
        # assert file is not None
        # with file:
        #     print(file.read())
        file = tar_file.extractfile(info)
        assert file is not None
        with file:
            sync_db_read(package, file)
    return db
