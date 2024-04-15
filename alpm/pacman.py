def user_agent_format(
    pacman_version: str, sysname: str, machine: str, alpm_version: str
):
    return f"pacman/{pacman_version} ({sysname} {machine}) libalpm/{alpm_version}"
