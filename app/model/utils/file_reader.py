def read_file(name: str, encoding: str = 'utf-8'):
    """
    :param name: относительный или полный путь до файла
    :param encoding: кодировка (по умолчанию UTF-8)
    :return: содержимое файла
    """
    with open(file=name, mode='r', encoding=encoding) as file:
        return file.read()
