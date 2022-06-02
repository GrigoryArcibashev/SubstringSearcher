import urllib
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request


def load_content(url: str) -> Optional[bytes]:
    """
    Загружает содержимое и возвращает его как поток байтов

    :param url: URL, с которого загружается содержимое
    """
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(request, timeout=10).read()
    except (HTTPError, URLError):
        return None


def load_content_as_string(url: str) -> Optional[str]:
    """
    Загружает содержимое и возвращает его как строку

    :param url: URL, с которого загружается содержимое
    """
    content = load_content(url)
    return None if content is None else content.decode("utf-8")
