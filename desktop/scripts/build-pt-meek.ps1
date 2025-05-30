$env:MEEK_TAG = 'v0.38.0'

New-Item -ItemType Directory -Force -Path .\build\meek
cd .\build\meek
git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/meek.git
cd meek
git checkout $MEEK_TAG
go build .\meek-client
Move-Item -Path .\meek-client.exe -Destination ..\..\..\onionetwork\resources\tor\meek-client.exe
