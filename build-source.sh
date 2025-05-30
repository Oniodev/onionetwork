#!/bin/bash

# The script builds a source package

# Usage
display_usage() {
  echo "Usage: $0 [tag]"
}

if [ $# -lt 1 ]
then
  display_usage
  exit 1
fi

# Input validation
TAG=$1

if [ "${TAG:0:1}" != "v" ]
then
  echo "Tag must start with 'v' character"
  exit 1
fi

VERSION=${TAG:1}

# Make sure tag exists
git tag | grep "^$TAG\$"
if [ $? -ne 0 ]
then
  echo "Tag does not exist"
  exit 1
fi

# Clone source
mkdir -p build/source
mkdir -p dist
cd build/source
git clone --single-branch --branch $TAG --depth 1 https://github.com/onionetwork/onionetwork.git
cd onionetwork

# Verify tag
git tag -v $TAG 2> ../verify.txt
if [ $? -ne 0 ]
then
  echo "Tag does not verify"
  exit 1
fi
cat ../verify.txt | grep -e "using RSA key 927F419D7EC82C2F149C1BD1403C2657CD994F73" -e "using RSA key 2E530667425F4B93874935707B7F1772C0C6FCBF" -e "using RSA key 3804565A5EFA6C11AFDA0E5359B3F0C24135C6A9"
if [ $? -ne 0 ]
then
  echo "Tag signed with wrong key"
  exit 1
fi
cat ../verify.txt | grep "^gpg: Good signature from"
if [ $? -ne 0 ]
then
  echo "Tag verification missing 'Good signature from'"
  exit 1
fi

# Checkout code
git checkout $TAG

# Delete .git, compress, and PGP sign
cd ..
rm -rf onionetwork/.git
tar -czf onionetwork-$VERSION.tar.gz onionetwork/

# Move source package to dist
cd ../..
mv build/source/onionetwork-$VERSION.tar.gz dist

# Clean up
rm -rf build/source/onionetwork
rm build/source/verify.txt

echo "Source package complete, file in dist"
