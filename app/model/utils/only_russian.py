from string import whitespace
from typing import Optional

from bs4 import BeautifulSoup

from app.model.utils.url_loader import load_content


def get_russian_text_by_url(url: str) -> Optional[str]:
    """
    Берет содержимое тэгов <p> и <span> из html указанного url
    и вырезает из него только русский текст со знаками пунктуации
    """
    raw_html = load_content(url)
    if raw_html is None:
        return None
    tags = BeautifulSoup(raw_html, 'html.parser').findAll(['p', 'span'])
    chunks_of_text = filter(
        lambda text: text, map(lambda tag: tag.text, tags))
    return get_only_russian_text('\n\n'.join(chunks_of_text).strip())


def get_only_russian_text(text: str) -> str:
    """
    Возвращает исходный текст только с русскими буквами,
    цифрами и знаками препинания
    """
    russian_text: list[str] = list(filter(is_suitable_symbol, text))
    return ''.join(russian_text)


def is_suitable_symbol(symbol: str) -> bool:
    """Проверяет, является ли символ подходящим для отображения"""
    return (
        is_russian_letter(symbol)
        or is_whitespace(symbol)
        or is_punctuation(symbol)
        or symbol.isdigit()
    )


def is_russian_letter(symbol: str) -> bool:
    """Проверяет, является ли символ русской буквой"""
    return (
        ord('а') <= ord(symbol) <= ord('я')
        or ord('А') <= ord(symbol) <= ord('Я')
    )


def is_punctuation(symbol: str) -> bool:
    """Проверяет, является ли символ знаком пунктуации"""
    return symbol in """\"!\'(),-.:;?"""


def is_whitespace(symbol: str) -> bool:
    """Проверяет, является ли символ пробельным"""
    return symbol in whitespace
