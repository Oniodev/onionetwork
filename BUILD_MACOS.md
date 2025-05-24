# Building Onionetwork for macOS

This guide will help you build an Onionetwork .app bundle for macOS.

## Prerequisites

1. **macOS**: You need to be running macOS to build the .app bundle
2. **Python 3.10-3.12**: Install from [python.org](https://python.org) or via Homebrew
3. **Poetry**: Install with `pip install poetry`
4. **create-dmg**: Install with `brew install create-dmg`
5. **Command Line Tools**: Install with `xcode-select --install`

## Build Steps

### 1. Setup the Project

First, ensure you have all dependencies installed:

```bash
# Clone the repository (if you haven't already)
cd /path/to/onionetwork-main

# Install CLI dependencies
cd cli
poetry install

# Install Desktop dependencies
cd ../desktop
poetry install
```

### 2. Download Tor Binaries

You need to download the Tor binaries for macOS:

```bash
cd desktop
poetry run python scripts/get-tor.py macos
```

This will download the necessary Tor binaries for both Intel and Apple Silicon architectures.

### 3. Build the App Bundle

Now build the actual application:

```bash
# Still in the desktop directory
poetry run python setup-freeze.py bdist_mac
```

This will create the app bundle in `desktop/build/Onionetwork.app`.

### 4. Clean Up Unused Files (Optional but Recommended)

To reduce the app size, clean up unnecessary files:

```bash
poetry run python scripts/build-macos.py cleanup-build
```

### 5. Code Sign the App (Required for Distribution)

If you have an Apple Developer ID, you can sign the app:

```bash
poetry run python scripts/build-macos.py codesign build/Onionetwork.app
```

Note: You'll need to modify the `identity_name_application` variable in `scripts/build-macos.py` to match your Developer ID.

### 6. Create the DMG

Finally, create the distributable DMG file:

```bash
poetry run python scripts/build-macos.py package build/Onionetwork.app
```

This will create `desktop/dist/Onionetwork-{version}.dmg`.

## Quick Build Script

For convenience, here's a script that runs all the steps:

```bash
#!/bin/bash
cd desktop
poetry run python scripts/get-tor.py macos
poetry run python setup-freeze.py bdist_mac
poetry run python scripts/build-macos.py cleanup-build
# Uncomment the next line if you have code signing set up
# poetry run python scripts/build-macos.py codesign build/Onionetwork.app
poetry run python scripts/build-macos.py package build/Onionetwork.app
```

## Troubleshooting

1. **"create-dmg: command not found"**: Install it with `brew install create-dmg`
2. **Poetry errors**: Make sure you're using a compatible Python version (3.10-3.12)
3. **Code signing errors**: You need a valid Apple Developer ID certificate
4. **Build errors**: Try cleaning the build directory with `rm -rf build/` and starting over

## Testing the App

After building, you can test the app by:

1. Opening `desktop/build/Onionetwork.app` directly
2. Or mounting the DMG and running the app from there

The app should launch with the new Onionetwork branding and logo.
