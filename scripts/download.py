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
    "clean": "https://drive.google.com/uc?id=1f_qNLG_WwPAUqIeLlD4uxRK4T8oK8sx0",
}


# Project root directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))


# Paths to project directories.
PATHS = {
    "raw": os.path.join(ROOT, "data", "Cloud_Data",
                        "cbc_effort_weather_1900-2018.txt"),
    "clean": os.path.join(ROOT, "data", "Cloud_Data",
                        "1.0-rec-initial-data-cleaning.txt"),
}


def download_raw():
    """Download the raw Christmas Bird Count data."""
    download(URLS["raw"], PATHS["raw"])


def download_clean():
    """Download the cleaned Christmas Bird Count data.

    .. note::
       For reproducibility, it might be better to clean the raw data locally
       rather than downloading a cleaned version from the cloud.
    """
    download(URLS["clean"], PATHS["clean"])


def download(url, path):
    """Download project data from the cloud.

    Args:
        url (str): URL from which to fetch data.
        path (str): Directory in which to store data.
    """
    cwd = os.getcwd()
    os.chdir(os.path.dirname(path))
    gdown.download(url)
    os.chdir(cwd)


if __name__ == "__main__":
    # Make the data/raw/ directory if it doesn't exist.
    datadir = pathlib.Path(os.path.dirname(PATHS["raw"]))
    datadir.mkdir(parents=True, exist_ok=True)

    # Download the each file if it doesn't already exist.
    for file in ["raw", "clean"]:
        if os.path.isfile(PATHS[file]):
            print(PATHS[file], "already exists.")
        else:
            download(URLS[file], PATHS[file])
