# Installation Guide

## Quick Install

```bash
# 1. Clone repository
git clone <repo-url>
cd Cyber-AutoAgent

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Set API key
export OPENAI_API_KEY="your-api-key-here"

# 5. Test installation
python cli.py --list-modules
```

## Detailed Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- OpenAI API key

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Core packages installed:**
- `strands-agents` - Agent framework with OpenAI support (includes tools)
- `mem0ai` - Memory management
- `faiss-cpu` - Vector database
- `pyyaml` - Plugin configuration
- `python-dotenv` - Environment variables
- `openai` - OpenAI API client

### Step 2: Install Security Tools (Optional)

For full functionality, install security testing tools:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y nmap nikto sqlmap gobuster dirb whatweb
```

**macOS:**
```bash
brew install nmap nikto sqlmap gobuster dirb
```

**Kali Linux:**
```bash
# Most tools pre-installed
sudo apt update
sudo apt install -y gobuster
```

### Step 3: Configure API Key

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY="sk-..."
```

**Option B: .env File**
```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

**Option C: Command Line**
```bash
python cli.py --api-key "sk-..." --target <target> --objective <objective>
```

### Step 4: Verify Installation

```bash
# Check Python version
python3 --version  # Should be 3.10+

# List available modules
python cli.py --list-modules

# Test with help
python cli.py --help
```

## Troubleshooting

### "No module named 'strands'"

**Solution:**
```bash
pip install strands-agents>=1.11.0
```

### "No module named 'mem0'"

**Solution:**
```bash
pip install mem0ai
```

### "No module named 'faiss'"

**Solution:**
```bash
pip install faiss-cpu
```

### "ImportError: cannot import name 'shell'"

This usually means the strands package structure changed. The tool includes fallback imports.

**Solution:**
```bash
pip install --upgrade strands-agents
```

### Permission Errors on Linux

If you get permission errors:

```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: User install
pip install --user -r requirements.txt

# Option 3: Break system packages (not recommended)
pip install --break-system-packages -r requirements.txt
```

### "Command not found: nmap"

Security tools are optional but recommended:

```bash
# Ubuntu/Debian
sudo apt install nmap nikto sqlmap

# macOS
brew install nmap nikto sqlmap
```

## Virtual Environment Setup (Recommended)

Using a virtual environment prevents conflicts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## Docker Installation (Alternative)

If you prefer Docker:

```bash
# Build image
docker build -t cyber-autoagent .

# Run
docker run -it --rm \
  -e OPENAI_API_KEY="your-key" \
  cyber-autoagent \
  --target <target> --objective <objective>
```

## Upgrading

To upgrade to the latest version:

```bash
# Pull latest code
git pull

# Upgrade dependencies
pip install --upgrade -r requirements.txt
```

## Uninstalling

```bash
# Remove virtual environment
rm -rf venv

# Or uninstall packages
pip uninstall -r requirements.txt -y
```

## Platform-Specific Notes

### Windows (WSL2)

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Follow standard installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

```bash
# Install Python via Homebrew
brew install python@3.11

# Follow standard installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Linux

```bash
# Ensure Python 3.10+
python3 --version

# Install pip and venv if needed
sudo apt install python3-pip python3-venv

# Follow standard installation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Verification

After installation, verify everything works:

```bash
# List modules
python cli.py --list-modules

# Should show:
# - general (General Security Assessment)
# - ctf (CTF Challenge Solver)
# - code_security (Code Security Analysis)

# Check version
python cli.py --help

# Test with dummy target (will fail without API key, which is expected)
python cli.py --target test --objective test 2>&1 | grep "API key"
```

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review README.md
3. Check GitHub issues
4. Enable verbose mode: `python cli.py --verbose`

## Next Steps

After successful installation:

1. Read [README.md](README.md) for usage examples
2. Review [OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md) for performance tuning
3. Start with a safe test target like `http://testphp.vulnweb.com`
