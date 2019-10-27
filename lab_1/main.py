"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def read_from_file(path_to_file: str, lines_limit: int) -> str:
    text = ''
    if isinstance(path_to_file, str) and isinstance(lines_limit, int) and lines_limit >= 0:
        with open(path_to_file) as data:
            for _ in range(lines_limit):
                text += data.readline()
    return text


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    dict_of_freqs = {}
    if isinstance(text, str) and text != '':
        text = text.lower()
        for char in text:
            if not char.isalpha() and char != ' ':
                text = text.replace(char, ' ')
        dict_of_freqs = {elem: text.split().count(elem) for elem in text.split()}
    return dict_of_freqs


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from the given frequencies dictionary
    """
    freq_dict_str_only = {}
    if frequencies:
        freq_dict_str_only = {key: value for key, value in frequencies.items() if isinstance(key, str)}
        if stop_words:
            for elem in stop_words:
                if elem in freq_dict_str_only:
                    del freq_dict_str_only[elem]
    return freq_dict_str_only


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    top_words = ()
    if frequencies and top_n > 0:
        freqs_list = list(frequencies.items())
        freqs_list.sort(key=lambda i: i[1], reverse=True)
        if top_n >= len(frequencies):
            top_words = tuple([freqs_list[i][0] for i in range(len(frequencies))])
        else:
            top_words = tuple([freqs_list[i][0] for i in range(top_n)])
    return top_words


def write_to_file(path_to_file: str, content: tuple):
    if isinstance(path_to_file, str) and isinstance(content, tuple):
        with open(path_to_file, 'w') as file:
            for elem in content:
                elem += '\n'
                file.write(elem)
