#!/bin/bash
MEEK_TAG=v0.38.0

OS=$(uname -s)

mkdir -p ./build/meek
cd ./build/meek
git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/meek.git || echo "already cloned"
cd meek
git checkout $MEEK_TAG

if [ "$OS" == "Darwin" ]; then
    if [[ $(uname -m) == 'arm64' ]]; then
        go build -o ../../../onionetwork/resources/tor/meek-client-arm64 ./meek-client
        GOOS=darwin GOARCH=amd64 go build -o ../../../onionetwork/resources/tor/meek-client-amd64 ./meek-client
        lipo -create -output ../../../onionetwork/resources/tor/meek-client ../../../onionetwork/resources/tor/meek-client-arm64 ../../../onionetwork/resources/tor/meek-client-amd64
        rm ../../../onionetwork/resources/tor/meek-client-arm64 ../../../onionetwork/resources/tor/meek-client-amd64
    elif [[ $(uname -m) == 'x86_64' ]]; then
        go build -o ../../../onionetwork/resources/tor/meek-client ./meek-client
    fi
else
    go build -o ../../../onionetwork/resources/tor/meek-client ./meek-client
fi
