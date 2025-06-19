from setuptools.command.build_py import build_py
import subprocess
from pathlib import Path

class BuildWithManifest(build_py):
    """Custom build command that updates manifest and state before packaging."""
    def run(self):
        repo_root = Path(__file__).resolve().parents[2]
        script = repo_root / 'scripts' / 'update-reference.zsh'
        subprocess.check_call([str(script)])
        super().run()
