"""Dagger module for Pepperpy Poetry Plugin."""
import dagger
from dagger import dag, function, object_type


@object_type
class PepperpyPoetry:
    """Dagger module for Pepperpy Poetry Plugin."""

    @function
    async def build_docs(self, source_dir: str = "docs") -> dagger.Container:
        """Build documentation using MkDocs.
        
        Args:
            source_dir: Directory containing documentation source files.
        """
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "poetry"])
            .with_mounted_directory("/src", dag.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "install", "--with", "docs"])
            .with_exec(["poetry", "run", "mkdocs", "build", "--config-file", f"{source_dir}/mkdocs.yml"])
        )

    @function
    async def deploy_docs(self, source_dir: str = "docs") -> dagger.Container:
        """Deploy documentation to GitHub Pages.
        
        Args:
            source_dir: Directory containing documentation source files.
        """
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_exec(["pip", "install", "poetry"])
            .with_mounted_directory("/src", dag.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "install", "--with", "docs"])
            .with_exec(["poetry", "run", "mkdocs", "gh-deploy", "--config-file", f"{source_dir}/mkdocs.yml"])
        ) 