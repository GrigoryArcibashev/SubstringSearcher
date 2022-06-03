from typing import Optional
from urllib.error import HTTPError, URLError

import requests


def load_content(url: str) -> Optional[str]:
    """
    Загружает содержимое и возвращает его как строку

    :param url: URL, с которого загружается содержимое
    """
    try:
        return requests.get(url).text
    except (HTTPError, URLError):
        return None
