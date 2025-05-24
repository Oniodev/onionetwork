#!/bin/bash
OS=$(uname -s)

if [ "$OS" == "Linux" ]; then
    # Check poetry installation and exit if no installation found.
    if ! command -v poetry 2>&1 >/dev/null
    then
        echo "Could not detect Poetry installation. Please make sure you install Poetry first.
        See https://python-poetry.org/docs/#installation or run pip3 install poetry"
        exit 1
    fi

    # Check golang installation and exit if no installation found.
    if ! command -v go 2>&1 >/dev/null
    then
        echo "Could not detect Go installation. Please make sure you install Go first.
        See https://go.dev/doc/install"
        exit 1
    fi

    # setup environment
    cd cli
    poetry install
    echo "Onionetwork CLI is installed!"
    cd ../desktop
    poetry install

    # setup tor
    poetry run python ./scripts/get-tor.py linux-x86_64
    echo "Tor is installed"

    # compile dependencies
    ./scripts/build-pt-obfs4proxy.sh
    ./scripts/build-pt-snowflake.sh
    ./scripts/build-pt-meek.sh

    # add alias
    echo "alias onionetwork='cd $(pwd) && poetry run onionetwork'" >> ~/.bash_aliases
    echo "alias onionetwork-cli='cd $(pwd) && poetry run onionetwork-cli'" >> ~/.bash_aliases
    source ~/.bash_aliases

    echo "Onionetwork Desktop is now installed"
    echo "Try running 'onionetwork' to start onionetwork server from source tree"
    echo "Restart a new terminal if the above doesnt work"
    echo "Checkout desktop/README.md for more info"
else
    echo "This script only works in linux distros, Try cli/README.md, desktop/README.md for installation steps"
    exit 1
fi
