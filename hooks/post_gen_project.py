import os
import subprocess
import sys


def setup_git() -> None:
    """Set up the git repository."""
    # Initialize the git repository
    try:
        subprocess.run(["git", "init", "."], check=True)
    except subprocess.CalledProcessError:
        print(
            "ERROR: Unable to initialize git repository. "
            "Make sure that 'git' is properly installed on your system."
        )
        sys.exit(os.EX_CANTCREAT)
    # Set up pre-commit hooks
    try:
        subprocess.run(["pre-commit", "install"], check=True)
    except subprocess.CalledProcessError:
        print(
            "ERROR: Unable to set up pre-commit hooks. "
            "Make sure that 'pre-commit' is properly installed on your system."
        )
        sys.exit(os.EX_CANTCREAT)


if __name__ == "__main__":
    setup_git()
    sys.exit(os.EX_OK)
