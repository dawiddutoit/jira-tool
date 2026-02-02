#!/usr/bin/env python3
"""
Build and Install jira-tool locally
This script builds the jira-tool package and installs it for system-wide use
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_colored(message: str, color: str) -> None:
    """Print a colored message to stdout"""
    print(f"{color}{message}{Colors.NC}")


def print_step(step: int, total: int, message: str) -> None:
    """Print a step header"""
    print_colored(f"[{step}/{total}] {message}", Colors.YELLOW)


def print_success(message: str) -> None:
    """Print a success message"""
    print_colored(f"✓ {message}", Colors.GREEN)


def print_error(message: str) -> None:
    """Print an error message"""
    print_colored(f"✗ {message}", Colors.RED)


def run_command(
    cmd: list[str], error_msg: str, check: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and handle errors"""
    try:
        result = subprocess.run(cmd, check=check, capture_output=False)
        return result
    except subprocess.CalledProcessError as e:
        print_error(error_msg)
        sys.exit(1)


def check_uv_installed() -> None:
    """Check if uv is installed"""
    if not shutil.which("uv"):
        print_error("Error: uv is not installed")
        print("Please install uv: https://github.com/astral-sh/uv")
        sys.exit(1)


def clean_build_artifacts() -> None:
    """Remove previous build artifacts"""
    artifacts = ["dist", "build"]
    project_root = Path(__file__).parent.parent

    for artifact in artifacts:
        artifact_path = project_root / artifact
        if artifact_path.exists():
            shutil.rmtree(artifact_path)

    # Clean egg-info directories
    for egg_info in project_root.rglob("*.egg-info"):
        shutil.rmtree(egg_info)


def sync_dependencies() -> None:
    """Sync project dependencies"""
    print_step(1, 6, "Syncing dependencies...")
    run_command(["uv", "sync"], "Failed to sync dependencies")
    print_success("Dependencies synced")
    print()


def run_linter(skip: bool) -> None:
    """Run the linter"""
    if skip:
        print_step(2, 6, "Skipping linter (--skip-lint)")
        print()
        return

    print_step(2, 6, "Running linter...")
    run_command(
        ["uv", "run", "ruff", "check", "src/", "tests/"],
        "Linting failed. Fix errors or use --skip-lint to bypass",
    )
    print_success("Linting passed")
    print()


def run_tests(skip: bool) -> None:
    """Run tests"""
    if skip:
        print_step(3, 6, "Skipping tests (--skip-tests)")
        print()
        return

    print_step(3, 6, "Running tests...")
    run_command(
        ["uv", "run", "pytest"],
        "Tests failed. Fix tests or use --skip-tests to bypass (not recommended)",
    )
    print_success("Tests passed")
    print()


def clean_builds() -> None:
    """Clean previous builds"""
    print_step(4, 6, "Cleaning previous builds...")
    clean_build_artifacts()
    print_success("Cleaned")
    print()


def build_package() -> None:
    """Build the package"""
    print_step(5, 6, "Building package...")
    run_command(["uv", "build"], "Build failed")
    print_success("Package built successfully")
    print()


def install_with_uv() -> None:
    """Install using uv tool"""
    print("Using: uv tool install (recommended)")

    # Uninstall first if it exists
    subprocess.run(
        ["uv", "tool", "uninstall", "jira-tool"],
        check=False,
        capture_output=True,
    )

    # Install from local directory
    run_command(
        ["uv", "tool", "install", "."],
        "Installation failed",
    )
    print_success("Installed via uv tool")
    print()
    print_colored("The 'jira-tool' command is now available system-wide", Colors.BLUE)
    print_colored("Run: jira-tool --help", Colors.BLUE)


def install_with_pip() -> None:
    """Install using pip"""
    print("Using: pip install --user")

    # Uninstall first if it exists
    subprocess.run(
        ["pip", "uninstall", "-y", "jira-tool"],
        check=False,
        capture_output=True,
    )

    # Get the wheel file
    dist_dir = Path(__file__).parent.parent / "dist"
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print_error("No wheel file found in dist/")
        sys.exit(1)

    wheel_file = wheel_files[0]
    run_command(
        ["pip", "install", "--user", str(wheel_file)],
        "Installation failed",
    )
    print_success("Installed via pip (user install)")
    print()
    print_colored("The 'jira-tool' command should be available", Colors.BLUE)
    print_colored(
        "Note: Make sure ~/.local/bin is in your PATH",
        Colors.YELLOW,
    )


def install_with_pipx() -> None:
    """Install using pipx"""
    if not shutil.which("pipx"):
        print_error("Error: pipx is not installed")
        print("Install pipx: python -m pip install --user pipx")
        sys.exit(1)

    print("Using: pipx install")

    # Uninstall first if it exists
    subprocess.run(
        ["pipx", "uninstall", "jira-tool"],
        check=False,
        capture_output=True,
    )

    # Install from local directory
    run_command(
        ["pipx", "install", "."],
        "Installation failed",
    )
    print_success("Installed via pipx")
    print()
    print_colored("The 'jira-tool' command is now available system-wide", Colors.BLUE)


def install_package(method: str) -> None:
    """Install the package using the specified method"""
    print_step(6, 6, "Installing jira-tool locally...")

    if method == "uv":
        install_with_uv()
    elif method == "pip":
        install_with_pip()
    elif method == "pipx":
        install_with_pipx()
    else:
        print_error(f"Unknown install method '{method}'")
        print("Valid options: uv, pip, pipx")
        sys.exit(1)


def print_completion_message() -> None:
    """Print completion message with usage info"""
    print()
    print_colored("=" * 40, Colors.GREEN)
    print_colored("  Installation Complete! 🎉", Colors.GREEN)
    print_colored("=" * 40, Colors.GREEN)
    print()
    print("Quick start:")
    print("  jira-tool --help              # Show all commands")
    print("  jira-tool get PROJ-123        # Get an issue")
    print("  jira-tool search 'project=X'  # Search issues")
    print()
    print("Configuration required (set in ~/.bashrc or ~/.zshrc):")
    print("  export JIRA_BASE_URL='https://your-domain.atlassian.net'")
    print("  export JIRA_USERNAME='your-email@example.com'")
    print("  export JIRA_API_TOKEN='your-api-token'")
    print()


def main() -> None:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Build and install jira-tool locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests before build",
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip running linter before build",
    )
    parser.add_argument(
        "--install-method",
        choices=["uv", "pip", "pipx"],
        default="uv",
        help="Installation method (default: uv)",
    )

    args = parser.parse_args()

    print_colored("=" * 40, Colors.BLUE)
    print_colored("  Building and Installing jira-tool", Colors.BLUE)
    print_colored("=" * 40, Colors.BLUE)
    print()

    check_uv_installed()
    sync_dependencies()
    run_linter(args.skip_lint)
    run_tests(args.skip_tests)
    clean_builds()
    build_package()
    install_package(args.install_method)
    print_completion_message()


if __name__ == "__main__":
    main()
