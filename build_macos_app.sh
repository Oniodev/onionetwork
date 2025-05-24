#!/bin/bash

# Quick build script for Onionetwork macOS app
# Run this from the root directory of the project

set -e

echo "Building Onionetwork for macOS..."

# Make sure we're in the right directory
if [ ! -f "desktop/pyproject.toml" ]; then
    echo "Error: Please run this script from the root directory of the onionetwork project"
    exit 1
fi

# Check dependencies
if ! command -v poetry &> /dev/null; then
    echo "Error: Poetry is not installed. Please install poetry first."
    exit 1
fi

if ! command -v create-dmg &> /dev/null; then
    echo "Error: create-dmg is not installed. Please install with 'brew install create-dmg'"
    exit 1
fi

echo "Installing dependencies..."
cd cli
poetry install
cd ../desktop
poetry install

echo "Downloading Tor binaries..."
poetry run python scripts/get-tor.py macos

echo "Building app bundle..."
poetry run python setup-freeze.py bdist_mac

echo "Cleaning up unused files..."
poetry run python scripts/build-macos.py cleanup-build

echo "Creating DMG..."
poetry run python scripts/build-macos.py package build/Onionetwork.app

echo ""
echo "Build complete!"
echo "App bundle: desktop/build/Onionetwork.app" 
echo "DMG file: desktop/dist/Onionetwork-*.dmg"
echo ""
echo "To code sign the app (requires Apple Developer ID), run:"
echo "cd desktop && poetry run python scripts/build-macos.py codesign build/Onionetwork.app" 