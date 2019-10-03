"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def read_from_file(path_to_file: str, lines_limit: int) -> str:
    text = ''
    if isinstance(path_to_file, str) and isinstance(lines_limit, int) and lines_limit >= 0:
        with open(path_to_file) as data:
            for i in range(lines_limit):
                text += data.readline()
    return text

# path_to_file = 'C:\\data.txt'
# lines_limit = 5
# print(read_from_file(path_to_file, lines_limit))


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    if not isinstance(text, str) \
            or text == '' \
            or (not text.isalpha() and text.count(' ') == 0):
        return {}
    text = text.lower()
    for char in text:
        if char == ' ':
            continue
        if not char.isalpha():
            text = text.replace(char, '')
    list_of_words = text.split()
    dict_of_freqs = {}
    for elem in list_of_words:
        if elem in dict_of_freqs:
            dict_of_freqs[elem] += 1
        else:
            dict_of_freqs[elem] = 1
    return dict_of_freqs


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from the given frequencies dictionary
    """
    if not isinstance(frequencies, dict) \
            or frequencies == {}:
        return {}
    freq_dict_str_only = {}
    for key, value in frequencies.items():
        if isinstance(key, str):
            freq_dict_str_only[key] = value
    if not isinstance(stop_words, tuple):
        return freq_dict_str_only
    for elem in stop_words:
        while elem in freq_dict_str_only:
            del freq_dict_str_only[elem]
    return freq_dict_str_only


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    if frequencies == {} or top_n <= 0:
        return ()
    freqs_list = list(frequencies.items())
    top_words = ()
    if top_n >= len(frequencies):
        for i in range(len(frequencies)):
            top_words += (freqs_list[i][0],)
        return top_words
    for i in range(top_n):
        top_words += (freqs_list[i][0],)
    return top_words
