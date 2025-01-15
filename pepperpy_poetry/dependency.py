"""Dependency management utilities."""
from typing import List, Optional, Tuple

from cleo.io.io import IO
from poetry.core.packages.dependency import Dependency
from poetry.core.packages.package import Package
from poetry.factory import Factory
from poetry.repositories.pypi_repository import PyPiRepository


def get_latest_version(package_name: str) -> Optional[str]:
    """Get the latest version of a package from PyPI."""
    repository = PyPiRepository()
    packages = repository.find_packages(package_name)
    if not packages:
        return None
    return str(packages[0].version)


def update_dependencies(
    packages: Optional[Tuple[str, ...]] = None,
    check_only: bool = False,
    io: Optional[IO] = None
) -> int:
    """Update project dependencies."""
    try:
        poetry = Factory().create_poetry()
        pyproject = poetry.file
        
        if not packages:
            # Update all dependencies
            dependencies = list(poetry.package.requires)
            dev_dependencies = list(poetry.package.dev_requires)
            all_deps = dependencies + dev_dependencies
        else:
            # Update specific packages
            all_deps = []
            for package_name in packages:
                dep = next(
                    (d for d in poetry.package.requires if d.name == package_name),
                    next(
                        (d for d in poetry.package.dev_requires if d.name == package_name),
                        None
                    )
                )
                if dep:
                    all_deps.append(dep)
                else:
                    if io:
                        io.write_error(f"<error>Package {package_name} not found</error>")
                    return 1

        updates = []
        for dep in all_deps:
            latest = get_latest_version(dep.name)
            if latest and latest != str(dep.constraint):
                updates.append((dep.name, str(dep.constraint), latest))

        if not updates:
            if io:
                io.write_line("<info>All dependencies are up to date</info>")
            return 0

        if io:
            io.write_line("<info>Available updates:</info>")
            for name, current, latest in updates:
                io.write_line(f"  {name}: {current} -> {latest}")

        if check_only:
            return 0

        # Update dependencies in pyproject.toml
        content = pyproject.read()
        for name, current, latest in updates:
            content = content.replace(
                f'"{name}" = "^{current}"',
                f'"{name}" = "^{latest}"'
            )
            content = content.replace(
                f'"{name}" = "{current}"',
                f'"{name}" = "{latest}"'
            )

        pyproject.write(content)

        if io:
            io.write_line("<info>Dependencies updated successfully</info>")
        return 0

    except Exception as e:
        if io:
            io.write_error(f"<error>Error updating dependencies: {str(e)}</error>")
        return 1 