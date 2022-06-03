from app.model.utils.file_reader import read_file

long_string_of_one_char: str = 'a' * 16000

try:
    war_and_peace: str = read_file("war_and_peace.txt")
except FileNotFoundError:
    war_and_peace: str = read_file(r"./performance_tests/war_and_peace.txt")
