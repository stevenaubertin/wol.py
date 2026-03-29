# Wake-on-LAN

## Synopsis

A Python 3 CLI that sends the [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN) magic packet over UDP broadcast to wake a sleeping computer.

## Requirements

- Python 3.9+
- Node.js (for Husky pre-commit hooks)

## Usage

Clone this repository and run `wol.py` with the MAC address of the target:

```bash
# Clone this repository
git clone https://github.com/stevenaubertin/wol.py
cd wol.py

# Run the app
python wol.py -m AA:BB:CC:DD:EE:FF
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `-m` | MAC address (required) | — |
| `-i` | Broadcast IP address | `255.255.255.255` |
| `-p` | Port (`0`, `7`, or `9`) | `9` |
| `-v` | Verbose output | off |
| `-h` | Show help message | — |

### Examples

```bash
# Basic usage
python wol.py -m AA:BB:CC:DD:EE:FF

# Specify broadcast IP and port
python wol.py -m AA:BB:CC:DD:EE:FF -i 192.168.1.255 -p 7

# Verbose output
python wol.py -m AA:BB:CC:DD:EE:FF -v

# Show help
python wol.py -h
```

### Pre-flight Validation

Before sending the magic packet, the following checks are performed:

- **MAC address** — must be six colon-separated hex octets (e.g. `AA:BB:CC:DD:EE:FF`)
- **IP address** — must be a valid IPv4 address
- **Port** — must be one of `0`, `7`, or `9`

Invalid inputs raise a clear error message and the packet is not sent.

## Development

### Setup

```bash
# Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Install Husky pre-commit hooks
npm install
```

### Running Tests

```bash
python -m pytest test_wol.py -v
```

### Linting

```bash
python -m flake8 . --exclude=.venv,node_modules
```

### Pre-commit Hooks

Husky runs the following checks before each commit:

1. **flake8** — blocks on syntax errors and undefined names
2. **pytest** — blocks if any test fails

## License

[MIT](LICENSE)
