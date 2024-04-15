import dataclasses
import enum


class DependencyModifier(enum.Enum):
    ANY = enum.auto()
    EQ = enum.auto()
    GE = enum.auto()
    LE = enum.auto()
    GT = enum.auto()
    LT = enum.auto()


@dataclasses.dataclass
class Dependency:
    name: bytes
    version: bytes
    description: bytes | None
    modifier: DependencyModifier


def dependency_from_string(dependency_string: bytes):
    if (description_needle := dependency_string.find(b": ")) == -1:
        description_needle = len(dependency_string)
        description_start = description_needle
    else:
        description_start = description_needle + len(b": ")

    if (modifier_start := dependency_string.find(b"<", 0, description_needle)) != -1:
        if dependency_string.startswith(
            b"=", modifier_start + len(b"<"), description_needle
        ):
            modifier = DependencyModifier.LE
            version_start = modifier_start + len(b"<=")
        else:
            modifier = DependencyModifier.LT
            version_start = modifier_start + len(b"<")
    elif (modifier_start := dependency_string.find(b">", 0, description_needle)) != -1:
        if dependency_string.startswith(
            b"=", modifier_start + len(b">"), description_needle
        ):
            modifier = DependencyModifier.GE
            version_start = modifier_start + len(b">=")
        else:
            modifier = DependencyModifier.GT
            version_start = modifier_start + len(b">")
    elif (modifier_start := dependency_string.find(b"=", 0, description_needle)) != -1:
        modifier = DependencyModifier.EQ
        version_start = modifier_start + len(b"=")
    else:
        modifier_start = description_needle
        modifier = DependencyModifier.ANY
        version_start = modifier_start
    return Dependency(
        name=dependency_string[:modifier_start],
        version=dependency_string[version_start:description_needle],
        description=dependency_string[description_start:],
        modifier=modifier,
    )
