# alpm-py

Parse arch linux pacman database files.

usage:

```python
import tarfile

import alpm.backend_sync

with tarfile.open("/var/lib/pacman/sync/core.files") as file:
    db = alpm.backend_sync.tar_file_to_packages({}, file)
    print(db[b"base"])
```

output:

```
Package(filename=b'base-3-2-any.pkg.tar.zst', base=b'base', name=b'base', version=b'3', release=b'2', description=b'Minimal package set to define a basic Arch Linux installation', url=b'https://www.archlinux.org', packager=b'Jan Alexander Steffens (heftig) <heftig@archlinux.org>', md5sum=b'9fde97a64c7825c959d498235cede216', sha256sum=b'25da12f0347e4bef6c215dcd32b6495beb86010a8c7e40828167b95f56639061', base64_signature=b'iIsEABYIADMWIQQGaHodnU+rCLUP2Ss7lKgOUKR3xwUCZSIDFBUcaGVmdGlnQGFyY2hsaW51eC5vcmcACgkQO5SoDlCkd8ejAAEAtnDSI0OslAAJZP5UxL3lPSvlE/X6+J3PLjBH06lWBA8A/2bZk6Fh9gmVXSRxW8Pd/EDkdduDTRyTsPVYh9QswtIB', architecture=b'any', build_date=1696727741, compressed_size=2362, installed_size=0, licenses=[b'GPL'], replaces=[], groups=[], depends=[Dependency(name=b'filesystem', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'gcc-libs', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'glibc', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'bash', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'coreutils', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'file', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'findutils', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'gawk', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'grep', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'procps-ng', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'sed', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'tar', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'gettext', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'pciutils', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'psmisc', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'shadow', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'util-linux', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'bzip2', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'gzip', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'xz', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'licenses', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'pacman', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'archlinux-keyring', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'systemd', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'systemd-sysvcompat', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'iputils', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>), Dependency(name=b'iproute2', version=b'', description=b'', modifier=<DependencyModifier.ANY: 1>)], optional_depends=[Dependency(name=b'linux', version=b'', description=b'bare metal support', modifier=<DependencyModifier.ANY: 1>)], check_depends=[], make_depends=[], conflicts=[], provides=[], files=(), extended_data=[])
```

pprint

```python
pprint.pprint((db[b"base"]))
```

```
Package(filename=b'base-3-2-any.pkg.tar.zst',
        base=b'base',
        name=b'base',
        version=b'3',
        release=b'2',
        description=b'Minimal package set to define a basic Arch Linux install'
                    b'ation',
        url=b'https://www.archlinux.org',
        packager=b'Jan Alexander Steffens (heftig) <heftig@archlinux.org>',
        md5sum=b'9fde97a64c7825c959d498235cede216',
        sha256sum=b'25da12f0347e4bef6c215dcd32b6495beb86010a8c7e40828167b95f'
                  b'56639061',
        base64_signature=b'iIsEABYIADMWIQQGaHodnU+rCLUP2Ss7lKgOUKR3xwUCZSIDFBUc'
                         b'aGVmdGlnQGFyY2hsaW51eC5vcmcACgkQO5SoDlCkd8ejAAEAtnDS'
                         b'I0OslAAJZP5UxL3lPSvlE/X6+J3PLjBH06lWBA8A/2bZk6Fh9gmV'
                         b'XSRxW8Pd/EDkdduDTRyTsPVYh9QswtIB',
        architecture=b'any',
        build_date=1696727741,
        compressed_size=2362,
        installed_size=0,
        licenses=[b'GPL'],
        replaces=[],
        groups=[],
        depends=[Dependency(name=b'filesystem',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'gcc-libs',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'glibc',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'bash',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'coreutils',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'file',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'findutils',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'gawk',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'grep',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'procps-ng',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'sed',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'tar',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'gettext',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'pciutils',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'psmisc',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'shadow',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'util-linux',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'bzip2',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'gzip',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'xz',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'licenses',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'pacman',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'archlinux-keyring',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'systemd',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'systemd-sysvcompat',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'iputils',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>),
                 Dependency(name=b'iproute2',
                            version=b'',
                            description=b'',
                            modifier=<DependencyModifier.ANY: 1>)],
        optional_depends=[Dependency(name=b'linux',
                                     version=b'',
                                     description=b'bare metal support',
                                     modifier=<DependencyModifier.ANY: 1>)],
        check_depends=[],
        make_depends=[],
        conflicts=[],
        provides=[],
        files=(),
        extended_data=[])
```

check sha256:

```python
assert (
    hashlib.sha256(
        pathlib.Path(
            "/var/cache/pacman/pkg", db[b"base"].filename.decode()
        ).read_bytes()
    )
    .digest()
    .hex()
    == db[b"base"].sha256sum.decode()
)
```
