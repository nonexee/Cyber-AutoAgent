# Cyber-AutoAgent - Simple CLI

A minimal autonomous security assessment tool using Claude via Anthropic API.

## ⚠️ WARNING

**THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY**

- Use only on systems you own or have explicit written permission to test
- Ensure compliance with all applicable laws and regulations
- Deploy in safe, sandboxed environments
- You are fully responsible for how you use this tool

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install security tools (optional, but recommended)
# Ubuntu/Debian:
sudo apt install nmap nikto sqlmap

# macOS:
brew install nmap nikto sqlmap
```

### 2. Set API Key

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or create a .env file:
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### 3. Run Assessment

```bash
python cli.py \
  --target "http://testphp.vulnweb.com" \
  --objective "Find SQL injection vulnerabilities" \
  --max-iterations 30
```

## Usage

```bash
python cli.py --help

options:
  --target TARGET           Target system to assess (REQUIRED)
  --objective OBJECTIVE     Security assessment objective (REQUIRED)
  --max-iterations N        Maximum tool executions (default: 50)
  --model MODEL            Claude model (default: claude-3-5-sonnet-20241022)
  --api-key KEY            Anthropic API key (or set env var)
  --verbose                Enable debug logging
```

## Examples

### Basic Web Application Scan

```bash
python cli.py \
  --target "http://example.com" \
  --objective "Identify web vulnerabilities"
```

### Network Reconnaissance

```bash
python cli.py \
  --target "192.168.1.0/24" \
  --objective "Map network and identify open services"
```

### Verbose Mode

```bash
python cli.py \
  --target "http://test.local" \
  --objective "Security assessment" \
  --verbose
```

## How It Works

1. **Agent Creation**: Creates a Claude-powered agent with security tools
2. **Reconnaissance**: Agent scans and enumerates the target
3. **Vulnerability Detection**: Identifies potential security issues
4. **Memory Storage**: Saves findings to local FAISS vector database
5. **Reporting**: Agent documents results when objective is met

## Output

Results are saved in:
- `outputs/<target>/memory/` - Vector database with findings
- Console output - Real-time progress and results

## Architecture

```
cli.py                      # Entry point
├── src/modules/
│   ├── agent.py           # Agent creation
│   ├── config.py          # Simple configuration
│   ├── memory.py          # FAISS-based memory
│   └── prompts.py         # System prompts
└── outputs/               # Assessment results
```

## Tools Available to Agent

- **shell** - Execute command-line security tools
- **editor** - Create/modify scripts and payloads
- **memory** - Store findings in persistent memory
- **stop** - Signal completion when objective is met

## Requirements

- Python 3.10+
- Anthropic API key
- Optional: Security tools (nmap, nikto, sqlmap, etc.)

## API Costs

This tool uses Claude via Anthropic API. Monitor your usage:
- Claude 3.5 Sonnet: ~$3 per million input tokens, ~$15 per million output tokens
- A typical assessment might use 50k-200k tokens (~$0.15-$3.00)

## Troubleshooting

### "API key not found"
Set `ANTHROPIC_API_KEY` environment variable or use `--api-key` flag

### "Command not found: nmap"
Install security tools via system package manager

### Memory errors
Ensure sufficient disk space in `outputs/` directory

## License

MIT License - See LICENSE file

## Disclaimer

This tool is provided for educational and authorized security testing purposes only.
Users are solely responsible for ensuring they have proper authorization before
testing any systems. The authors assume no liability for misuse.

---

**Remember: Always get written permission before testing any target.**
