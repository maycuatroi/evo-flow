from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

import evoflow


@evoflow.Step()
def open_browser(url: str = None, proxy: Proxy = None) -> dict:
    """
    Open Fire fox browser

    :rtype: dict
    :param url:
    :param proxy:
    :return: dict object
    """
    browser = webdriver.Firefox(proxy=proxy)
    browser.get(url)
    return {"browser": browser}


@evoflow.Step()
def setup_proxy(proxy_url: str = None):
    """

    :param proxy_url: "xx.xx.xx.xx:xxxx"
    :return:
    """
    proxy = None
    if proxy_url:
        proxy = Proxy(
            {
                "proxyType": ProxyType.MANUAL,
                "httpProxy": proxy_url,
                "ftpProxy": proxy_url,
                "sslProxy": proxy_url,
                "noProxy": "",  # set this value as desired
            }
        )
    return {"proxy": proxy}
