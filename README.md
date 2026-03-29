# Wake-on-LAN

## Synopsis

A Python 3 CLI that sends the [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN) magic packet over UDP broadcast to wake a sleeping computer.

## Requirements

- Python 3.9 - 3.13
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

| Flag | Long | Description | Default |
|------|------|-------------|---------|
| `-m` | `--mac` | MAC address (required) | — |
| `-i` | `--ip` | Broadcast IP address | `255.255.255.255` |
| `-p` | `--port` | Port (`0`, `7`, or `9`) | `9` |
| `-v` | `--verbose` | Verbose output | off |
| `-h` | `--help` | Show help message | — |

### Examples

```bash
# Basic usage
python wol.py -m AA:BB:CC:DD:EE:FF

# Long option names
python wol.py --mac AA:BB:CC:DD:EE:FF --ip 192.168.1.255 --port 7

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

If the magic packet cannot be delivered (e.g. network error), the program prints an error and exits with code `1`.

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
