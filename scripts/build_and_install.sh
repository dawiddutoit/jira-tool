#!/bin/bash
# Build and Install jira-tool locally
# This script builds the jira-tool package and installs it for system-wide use

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SKIP_TESTS=false
SKIP_LINT=false
INSTALL_METHOD="uv"  # Options: uv, pip, pipx

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-lint)
            SKIP_LINT=true
            shift
            ;;
        --install-method)
            INSTALL_METHOD="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-tests          Skip running tests before build"
            echo "  --skip-lint           Skip running linter before build"
            echo "  --install-method METHOD   Installation method: uv (default), pip, or pipx"
            echo "  --help                Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Building and Installing jira-tool${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv is not installed${NC}"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# Step 1: Sync dependencies and install package in editable mode
echo -e "${YELLOW}[1/6] Syncing dependencies...${NC}"
uv sync --all-extras
uv pip install -e .
echo -e "${GREEN}✓ Dependencies synced and package installed in editable mode${NC}"
echo ""

# Step 2: Run linter (optional)
if [ "$SKIP_LINT" = false ]; then
    echo -e "${YELLOW}[2/6] Running linter...${NC}"
    uv run ruff check src/ tests/ || {
        echo -e "${RED}✗ Linting failed${NC}"
        echo "Fix linting errors or use --skip-lint to bypass"
        exit 1
    }
    echo -e "${GREEN}✓ Linting passed${NC}"
    echo ""
else
    echo -e "${YELLOW}[2/6] Skipping linter (--skip-lint)${NC}"
    echo ""
fi

# Step 3: Run tests (optional)
if [ "$SKIP_TESTS" = false ]; then
    echo -e "${YELLOW}[3/6] Running tests...${NC}"
    uv run pytest || {
        echo -e "${RED}✗ Tests failed${NC}"
        echo "Fix tests or use --skip-tests to bypass (not recommended)"
        exit 1
    }
    echo -e "${GREEN}✓ Tests passed${NC}"
    echo ""
else
    echo -e "${YELLOW}[3/6] Skipping tests (--skip-tests)${NC}"
    echo ""
fi

# Step 4: Clean previous builds
echo -e "${YELLOW}[4/6] Cleaning previous builds...${NC}"
rm -rf dist/ build/ *.egg-info src/*.egg-info
echo -e "${GREEN}✓ Cleaned${NC}"
echo ""

# Step 5: Build package
echo -e "${YELLOW}[5/6] Building package...${NC}"
uv build
echo -e "${GREEN}✓ Package built successfully${NC}"
echo ""

# Step 6: Install locally
echo -e "${YELLOW}[6/6] Installing jira-tool locally...${NC}"

case $INSTALL_METHOD in
    uv)
        echo "Using: uv tool install (recommended)"
        # Uninstall first if it exists
        uv tool uninstall jira-tool 2>/dev/null || true
        # Install from local directory
        uv tool install .
        echo -e "${GREEN}✓ Installed via uv tool${NC}"
        echo ""
        echo -e "${BLUE}The 'jira-tool' command is now available system-wide${NC}"
        echo -e "${BLUE}Run: jira-tool --help${NC}"
        ;;
    pip)
        echo "Using: pip install --user"
        # Uninstall first if it exists
        pip uninstall -y jira-tool 2>/dev/null || true
        # Install from wheel
        WHEEL_FILE=$(ls dist/*.whl | head -n 1)
        pip install --user "$WHEEL_FILE"
        echo -e "${GREEN}✓ Installed via pip (user install)${NC}"
        echo ""
        echo -e "${BLUE}The 'jira-tool' command should be available${NC}"
        echo -e "${YELLOW}Note: Make sure ~/.local/bin is in your PATH${NC}"
        ;;
    pipx)
        if ! command -v pipx &> /dev/null; then
            echo -e "${RED}Error: pipx is not installed${NC}"
            echo "Install pipx: python -m pip install --user pipx"
            exit 1
        fi
        echo "Using: pipx install"
        # Uninstall first if it exists
        pipx uninstall jira-tool 2>/dev/null || true
        # Install from local directory
        pipx install .
        echo -e "${GREEN}✓ Installed via pipx${NC}"
        echo ""
        echo -e "${BLUE}The 'jira-tool' command is now available system-wide${NC}"
        ;;
    *)
        echo -e "${RED}Error: Unknown install method '$INSTALL_METHOD'${NC}"
        echo "Valid options: uv, pip, pipx"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Installation Complete! 🎉${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Quick start:"
echo "  jira-tool --help              # Show all commands"
echo "  jira-tool get PROJ-123        # Get an issue"
echo "  jira-tool search 'project=X'  # Search issues"
echo ""
echo "Configuration required (set in ~/.bashrc or ~/.zshrc):"
echo "  export JIRA_BASE_URL='https://your-domain.atlassian.net'"
echo "  export JIRA_USERNAME='your-email@example.com'"
echo "  export JIRA_API_TOKEN='your-api-token'"
echo ""
