import subprocess
import tempfile
import shutil
import os
from typing import List, Dict

def clone_repositories(username: str, repo_names: List[str], max_repos: int = 3) -> Dict[str, str]:
    """
    Shallow clones the top N repositories into temporary system folders.
    Returns a dict mapping: {"repo_name": "/path/to/cloned/folder"}
    """
    cloned_paths = {}

    for name in repo_names[:max_repos]:
        # 1. Create an isolated temporary folder in the OS temp directory
        temp_dir = tempfile.mkdtemp(prefix=f"gh_eval_{username}_{name}_")
        repo_url = f"https://github.com/{username}/{name}.git"

        try:
            # 2. Run git clone --depth 1 (only latest commit, minimal disk & network usage)
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30  # Safety timeout against massive repos
            )
            cloned_paths[name] = temp_dir
            print(f"[Cloner] Successfully cloned {name} -> {temp_dir}")

        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            print(f"[Cloner Error] Failed cloning {name}: {err}")
            shutil.rmtree(temp_dir, ignore_errors=True)

    return cloned_paths

def cleanup_cloned_repos(repo_paths: Dict[str, str]):
    """
    Deletes all temporary folders after analysis to prevent disk leaks.
    """
    for name, path in repo_paths.items():
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            print(f"[Cleanup] Removed temp folder for {name}")
