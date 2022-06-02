def get_only_russian_text(text: str) -> str:
    """Возвращает исходный текст с удаленными латинсикми буквами"""
    russian_text: list[str] = []
    for symbol in text:
        if not is_latin_symbol(symbol):
            russian_text.append(symbol)
    return "".join(russian_text)


def is_latin_symbol(symbol: str) -> bool:
    return ord("a") <= ord(symbol) <= ord("z") \
           or ord("A") <= ord(symbol) <= ord("Z")
