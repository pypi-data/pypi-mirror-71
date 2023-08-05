"""Install the runnow library."""

import os
from pathlib import Path

from setuptools import setup

DETECTED_VERSION = None
VERSION_FILEPATH = "VERSION"

if "VERSION" in os.environ:
    DETECTED_VERSION = os.environ["VERSION"]
    if "/" in DETECTED_VERSION:
        DETECTED_VERSION = DETECTED_VERSION.split("/")[-1]
if not DETECTED_VERSION and os.path.exists(VERSION_FILEPATH):
    DETECTED_VERSION = Path(VERSION_FILEPATH).read_text()
    if len(DETECTED_VERSION.split(".")) <= 3:
        if "BUILD_NUMBER" in os.environ:
            DETECTED_VERSION = f"{DETECTED_VERSION}.{os.environ['BUILD_NUMBER']}"
if not DETECTED_VERSION:
    raise RuntimeError("Error. Could not detect version.")
DETECTED_VERSION = DETECTED_VERSION.replace(".dev0", "")
if os.environ.get("BRANCH_NAME", "unknown") not in ["master", "refs/heads/master"]:
    DETECTED_VERSION = f"{DETECTED_VERSION}.dev0"

DETECTED_VERSION = DETECTED_VERSION.lstrip("v")
print(f"Detected version: {DETECTED_VERSION}")
Path(VERSION_FILEPATH).write_text(f"v{DETECTED_VERSION}")

setup(
    name="runnow",
    packages=["runnow"],
    version=DETECTED_VERSION,
    license="MIT",
    description="Runnow, an easy-to-use command runner that does all the things.",
    author="Aaron (AJ) Steers",
    author_email="aj.steers@slalom.com",
    url="https://www.github.com/aaronsteers/runnow",
    download_url="https://www.github.com/aaronsteers/runnow/archive",
    keywords=["DATAOPS", "LOGGING"],
    package_data={"": [VERSION_FILEPATH]},
    entry_points={
        "console_scripts": [
            # Register CLI commands:
            "runnow = runnow.runnow:main",
        ]
    },
    include_package_data=True,
    install_requires=[
        "logless",
    ],
    extras_require={},
    classifiers=[
        "Development Status :: 4 - Beta",  # "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
# Revert `.dev0` suffix
Path(VERSION_FILEPATH).write_text(f"v{DETECTED_VERSION.replace('.dev0', '')}")
