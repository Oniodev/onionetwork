#!/usr/bin/env python3
# This file is used to build the Snapcraft and Flatpak packages
import os
import setuptools

# The version must be hard-coded because Snapcraft won't have access to ../cli
version_filename = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "cli", "onionetwork_cli", "resources", "version.txt"
)
with open(version_filename) as f:
    version = f.read().strip()

setuptools.setup(
    name="onionetwork",
    version=version,
    author="Micah Lee",
    author_email="micah@micahflee.com",
    url="https://onionetwork.org",
    license="GPLv3",
    keywords="onion, share, onionetwork, tor, anonymous, web server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Topic :: Communications :: File Sharing",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
    ],
    packages=[
        "onionetwork",
        "onionetwork.tab",
        "onionetwork.tab.mode",
        "onionetwork.tab.mode.share_mode",
        "onionetwork.tab.mode.receive_mode",
        "onionetwork.tab.mode.website_mode",
        "onionetwork.tab.mode.chat_mode",
    ],
    package_data={
        "onionetwork": [
            "resources/*",
            "resources/countries/*",
            "resources/images/*",
            "resources/locale/*/*",
        ]
    },
    entry_points={
        "console_scripts": [
            "onionetwork = onionetwork:main",
            "onionetwork-cli = onionetwork_cli:main",
        ],
    },
)
