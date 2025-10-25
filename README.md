# Cyber-AutoAgent - Simple CLI

A minimal autonomous security assessment tool using OpenAI models with built-in optimizations for cost and performance.

## ⚠️ WARNING

**THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY**

- Use only on systems you own or have explicit written permission to test
- Ensure compliance with all applicable laws and regulations
- Deploy in safe, sandboxed environments
- You are fully responsible for how you use this tool

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# If you encounter permission errors on Linux:
# pip install -r requirements.txt --user
# OR use virtual environment (recommended above)

# Install security tools (optional, but recommended)
# Ubuntu/Debian:
sudo apt install nmap nikto sqlmap

# macOS:
brew install nmap nikto sqlmap
```

> **Note:** If you get errors about `strands-tools`, that's expected - tools are included in `strands-agents`. See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

### 2. Set API Key

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Or create a .env file:
echo "OPENAI_API_KEY=your-api-key-here" > .env
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
  --module MODULE          Security module: general, ctf, code_security (default: general)
  --list-modules           List available security modules
  --max-iterations N        Maximum tool executions (default: 50)
  --model MODEL            OpenAI model (default: gpt-4o, options: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo)
  --api-key KEY            OpenAI API key (or set env var)
  --verbose                Enable debug logging

  # Performance optimizations (all enabled by default)
  --no-cache               Disable prompt caching (not recommended)
  --no-streaming           Disable response streaming
  --no-parallel-tools      Disable parallel tool execution
```

## Security Modules

The tool supports different operation modes via plugins:

### Available Modules

```bash
# List all available modules
python cli.py --list-modules
```

**1. General Security Assessment** (`--module general`)
- Web application testing
- Network reconnaissance
- Vulnerability scanning
- OWASP Top 10 testing
- Tools: nmap, nikto, sqlmap, gobuster, nuclei

**2. CTF Challenge Solver** (`--module ctf`)
- Capture The Flag challenges
- Cryptography puzzles
- Reverse engineering
- Binary exploitation
- Forensics analysis
- Tools: strings, binwalk, hashcat, ghidra, radare2

**3. Code Security Analysis** (`--module code_security`)
- Static code analysis
- Vulnerability detection
- Dependency auditing
- Security code review
- Tools: bandit, semgrep, eslint, gosec

## Examples

### Web Application Security Test

```bash
python cli.py \
  --module general \
  --target "http://testphp.vulnweb.com" \
  --objective "Find SQL injection and XSS vulnerabilities"
```

### CTF Challenge

```bash
python cli.py \
  --module ctf \
  --target "challenge.bin" \
  --objective "Extract the flag from this binary"
```

### Code Security Review

```bash
python cli.py \
  --module code_security \
  --target "./src" \
  --objective "Find security vulnerabilities in Python code"
```

### Network Reconnaissance

```bash
python cli.py \
  --module general \
  --target "192.168.1.0/24" \
  --objective "Map network and identify services"
```

### Verbose Mode

```bash
python cli.py \
  --module general \
  --target "http://test.local" \
  --objective "Complete security assessment" \
  --verbose
```

### Performance Tuning

```bash
# Disable optimizations for debugging
python cli.py \
  --no-cache \
  --no-streaming \
  --no-parallel-tools \
  --target <target> \
  --objective <objective>

# Use cheaper model with all optimizations
python cli.py \
  --model gpt-3.5-turbo \
  --target <target> \
  --objective <objective>
```

## How It Works

1. **Agent Creation**: Creates an OpenAI-powered agent with security tools
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
│   ├── agent.py           # Agent creation with OpenAI
│   ├── config.py          # Simple configuration
│   ├── memory.py          # FAISS-based memory
│   ├── prompts.py         # System prompts
│   └── plugins.py         # Plugin system
├── plugins/               # Security modules
│   ├── general/          # Web & network security
│   │   ├── config.yaml   # Module metadata
│   │   └── prompt.md     # System prompt
│   ├── ctf/              # CTF challenges
│   └── code_security/    # Code analysis
└── outputs/               # Assessment results
```

## Tools Available to Agent

- **shell** - Execute command-line security tools
- **editor** - Create/modify scripts and payloads
- **memory** - Store findings in persistent memory
- **stop** - Signal completion when objective is met

## Requirements

- Python 3.10+
- OpenAI API key
- PyYAML for plugin system
- Optional: Security tools (nmap, nikto, sqlmap, etc.)

## Performance & Cost Optimizations

This tool includes **automatic optimizations** that reduce costs by ~50% and improve performance:

### Built-in Optimizations (Enabled by Default)

1. **💰 Prompt Caching** - Caches system messages across requests
   - **50% cost reduction** on repeated prompts
   - Particularly effective for long assessments

2. **⚡ Response Streaming** - Stream responses in real-time
   - Better user experience
   - See output immediately as it's generated

3. **🔄 Parallel Tool Execution** - Run multiple tools concurrently
   - **2-3x faster** for reconnaissance phases
   - Example: Run nmap + nikto + whatweb simultaneously

### API Costs

**With optimizations enabled (default):**
- GPT-4o: ~$1.25/M input, ~$10/M output (cached tokens)
- GPT-4 Turbo: ~$5/M input, ~$30/M output (cached tokens)
- GPT-3.5 Turbo: ~$0.25/M input, ~$1.50/M output (cached tokens)

**Typical assessment cost (with caching):**
- Small task (20k tokens): $0.05-0.25
- Medium task (100k tokens): $0.25-1.50
- Large task (500k tokens): $1.25-7.50

**Savings example:** A 100-iteration assessment that would cost $2.50 without caching costs only $1.25 with caching enabled (50% savings).

See [OPTIMIZATIONS.md](docs/OPTIMIZATIONS.md) for detailed performance tuning.

## Troubleshooting

### "API key not found"
Set `OPENAI_API_KEY` environment variable or use `--api-key` flag

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
