def read_file(name: str, encoding: str = 'utf-8'):
    with open(file=name, mode='r', encoding=encoding) as file:
        return file.read()