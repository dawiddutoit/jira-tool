# Build and Install Scripts

This directory contains scripts to build and install the `jira-tool` package locally for system-wide use.

## Available Scripts

### 1. `build_and_install.sh` (Bash)
Shell script for Unix-like systems (Linux, macOS).

**Usage:**
```bash
# Basic usage (recommended)
./scripts/build_and_install.sh

# Skip tests (faster, but not recommended)
./scripts/build_and_install.sh --skip-tests

# Skip linting
./scripts/build_and_install.sh --skip-lint

# Use different installation method
./scripts/build_and_install.sh --install-method pip
./scripts/build_and_install.sh --install-method pipx

# Show help
./scripts/build_and_install.sh --help
```

### 2. `build_and_install.py` (Python)
Cross-platform Python script (works on Windows, Linux, macOS).

**Usage:**
```bash
# Basic usage (recommended)
python scripts/build_and_install.py

# Or if executable:
./scripts/build_and_install.py

# Skip tests (faster, but not recommended)
python scripts/build_and_install.py --skip-tests

# Skip linting
python scripts/build_and_install.py --skip-lint

# Use different installation method
python scripts/build_and_install.py --install-method pip
python scripts/build_and_install.py --install-method pipx

# Show help
python scripts/build_and_install.py --help
```

## Installation Methods

The scripts support three installation methods:

### 1. `uv` (Default - Recommended)
Uses `uv tool install` to install the package in an isolated environment.

**Pros:**
- Isolated from system Python
- Automatic PATH management
- Easy updates and uninstalls
- No dependency conflicts

**Command:**
```bash
./scripts/build_and_install.sh --install-method uv
```

**Uninstall:**
```bash
uv tool uninstall jira-tool
```

### 2. `pip`
Uses `pip install --user` to install to the user directory.

**Pros:**
- Standard Python packaging
- Works with existing pip workflows

**Cons:**
- May conflict with system packages
- Requires `~/.local/bin` in PATH

**Command:**
```bash
./scripts/build_and_install.sh --install-method pip
```

**Uninstall:**
```bash
pip uninstall jira-tool
```

### 3. `pipx`
Uses `pipx` to install in an isolated environment (requires pipx to be installed).

**Pros:**
- Similar benefits to `uv`
- Widely used for CLI tools

**Cons:**
- Requires separate pipx installation

**Command:**
```bash
./scripts/build_and_install.sh --install-method pipx
```

**Uninstall:**
```bash
pipx uninstall jira-tool
```

## What the Scripts Do

1. **Sync Dependencies** - Ensures all required packages are installed
2. **Run Linter** - Checks code quality (can be skipped with `--skip-lint`)
3. **Run Tests** - Validates functionality (can be skipped with `--skip-tests`)
4. **Clean Builds** - Removes old build artifacts
5. **Build Package** - Creates distribution files (wheel and source)
6. **Install Locally** - Installs the package system-wide

## Post-Installation

After installation, the `jira-tool` command will be available system-wide:

```bash
# Verify installation
jira-tool --help

# Get an issue
jira-tool get PROJ-123

# Search issues
jira-tool search "project = MYPROJECT"
```

## Configuration

Set these environment variables in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export JIRA_BASE_URL='https://your-domain.atlassian.net'
export JIRA_USERNAME='your-email@example.com'
export JIRA_API_TOKEN='your-api-token'

# Optional
export JIRA_DEFAULT_PROJECT='MYPROJECT'
export JIRA_DEFAULT_COMPONENT='Component Name'
```

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

## Troubleshooting

### Command not found after installation

**For uv/pipx:**
- The tool directory should be automatically in your PATH
- Try `source ~/.bashrc` or `source ~/.zshrc` to reload your shell
- Or close and reopen your terminal

**For pip:**
- Ensure `~/.local/bin` is in your PATH
- Add to `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```

### Build fails

1. Ensure `uv` is installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Ensure you're in the project root directory

3. Try cleaning and rebuilding:
   ```bash
   rm -rf dist/ build/ *.egg-info
   ./scripts/build_and_install.sh
   ```

### Tests fail

If tests fail, investigate the failures. Only use `--skip-tests` if you're sure the failures are unrelated to your changes.

### Linting fails

Fix the linting errors with:
```bash
uv run black src/ tests/
uv run ruff check --fix src/ tests/
```

Or use `--skip-lint` to bypass (not recommended for production).

## Development Workflow

For active development, you don't need to reinstall after every change. Use:

```bash
# Run CLI directly during development
uv run jira-tool [command]

# Or activate the virtual environment
source .venv/bin/activate
jira-tool [command]
```

Only run the build and install scripts when you want to install a stable version system-wide.

## Updating the Installation

To update an existing installation:

```bash
# Pull latest changes
git pull

# Rebuild and reinstall
./scripts/build_and_install.sh
```

The scripts automatically uninstall the old version before installing the new one.
