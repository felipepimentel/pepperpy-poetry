"""Dagger module for Pepperpy Poetry Plugin."""
import dagger
from dagger import dag, function, object_type


@object_type
class PepperpyPoetry:
    """Dagger module for Pepperpy Poetry Plugin."""

    @function
    async def build_docs(self) -> dagger.Container:
        """Build documentation using MkDocs."""
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "poetry"])
            .with_mounted_directory("/src", dag.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "install", "--with", "docs"])
            .with_exec(["poetry", "run", "mkdocs", "build"])
        )

    @function
    async def deploy_docs(self) -> dagger.Container:
        """Deploy documentation to GitHub Pages."""
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "poetry"])
            .with_mounted_directory("/src", dag.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "install", "--with", "docs"])
            .with_exec(["poetry", "run", "mkdocs", "gh-deploy"])
        ) 