import pathlib
import urllib

import evoflow

try:
    from pyunpack import Archive
except ImportError:
    evoflow.logger.error(
        "Can't import pyunpack. Try to install with:\npip install pyunpack"
    )


def download_and_unzip(url: str, des_path: str, proxies_list: dict = None):
    if proxies_list is None:
        proxies_list = {}
    pathlib.Path(des_path).mkdir(parents=True, exist_ok=True)
    download_file_name = url.split("/")[-1]
    opener = urllib.request.URLopener(proxies=proxies_list)
    opener.addheader("User-Agent", "evoflow")
    filename, _ = opener.retrieve(url, f"{des_path}/{download_file_name}")
    Archive(filename).extractall(des_path)
    os.remove(filename)


if __name__ == "__main__":
    import os

    proxies = {
        "http": "fsoft-proxy:8080",
    }
    downloaded_path = f'{os.getenv("userprofile")}/.evoflow'
    download_and_unzip(
        "https://github.com/upx/upx/releases/download/v3.96/upx-3.96-win64.zip",
        downloaded_path,
        proxies_list=proxies,
    )
