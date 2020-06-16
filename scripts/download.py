"""Utilities for downloading project data.

Top level function :func:`scripts.download.download_raw` downloads the raw
Christmas Bird Count project data from Google Drive.

Run this module as a script to automatically download the project data into
``data/raw/`` under the project root. If the directory doesn't already exist,
this script will create it.

"""
import gdown
import os
import pathlib


# URLs for project data.
URLS = {
    "raw": "https://drive.google.com/uc?id=1vwC_m-wFaX-4brrHOrTVqVFDZDJ6y3gN",
}


# Project root directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


# Paths to project directories.
PATHS = {
    "raw": os.path.join(ROOT, "data", "Cloud_Data"),
}


def download_raw(url=None, path=None):
    """Download the raw Christmas Bird Count data.

    Args:
        url (str): URL from which to fetch raw data.
        path (str): Directory in which to store raw data.
    """
    # Use the standard URL by default.
    if not url:
        url = URLS["raw"]

    # Use the standard path by default.
    if not path:
        path = PATHS["raw"]
        
    cwd = os.getcwd()
    os.chdir(path)
    gdown.download(url)
    os.chdir(cwd)


if __name__ == "__main__":
    # Make the data/raw/ directory if it doesn't exist.
    pathlib.Path(PATHS["raw"]).mkdir(parents=True, exist_ok=True)

    # Download the raw data if the file doesn't already exist.
    filename = os.path.join(PATHS["raw"], "cbc_effort_weather_1900-2018.txt")
    if os.path.isfile(filename):
        print(filename, "already exists.")
    else:
        download_raw()
