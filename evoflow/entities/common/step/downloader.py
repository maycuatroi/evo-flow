import os
import pathlib
import shutil
from urllib.request import urlretrieve

import pandas as pd
import requests
from tqdm import tqdm

import evoflow
from evoflow import logger


class TqdmDownload(tqdm):
    """Alternative Class-based version of the above.
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize


@evoflow.Step()
def download_urls(urls: list = None, download_dir: str = "Downloads") -> object:
    """

    Args:
        urls (list, optional): List of urls to download. Defaults to None.
        download_dir (str, optional): Download directory. Defaults to 'Downloads'.
        download_paths (list, optional): List path to downloaded files. Defaults to None.
    Returns:
        dict: download_paths: List path to downloaded files

    """
    download_paths = []
    pathlib.Path(download_dir).mkdir(parents=True, exist_ok=True)
    progres_bar = tqdm(urls)

    for url in progres_bar:
        progres_bar.set_description(f"Downloading: {url}")
        try:
            res = requests.get(url)
            filename = "zasdvadf"
            with TqdmDownload(
                unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=filename
            ) as t:
                download_path, result = urlretrieve(
                    url, f"{download_dir}/miniconda.exe"
                )
                download_paths.append(download_path)

        except:
            logger.error(f"Can't access : {url}")

    return {"download_paths": download_path}


@evoflow.Step()
def download_urls(urls: list = None, download_dir: str = None) -> object:
    """
    @param urls: List of urls to download
    @param download_dir: Download directory
    @return: download_paths: List path to downloaded files
    @rtype: dict

    """
    download_paths = []
    df = pd.DataFrame(columns=["URL", "FILE_NAME"])
    if download_dir:
        pathlib.Path(download_dir).mkdir(parents=True, exist_ok=True)
    for i, url in tqdm(enumerate(urls), total=len(urls)):
        try:
            res = requests.get(url)
            with TqdmDownload(
                unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=url
            ) as t:
                download_path, result = urlretrieve(url)
                file_name = os.path.split(download_path)[1]
                if download_dir:
                    shutil.move(download_path, f"{download_dir}/{file_name}")
                    download_path = f"{download_dir}/{file_name}"
                download_paths.append(download_path)

            df.loc[i] = [url, download_path]
            df.to_csv(
                f"{download_dir}/downloader_log.csv", encoding="utf-8", index=False
            )
        except Exception as e:
            logger.error(f"{e}")

    return {"download_files": download_path}
