"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    if not isinstance(text, str) \
            or text == '' \
            or (not text.isalpha() and text.count(' ') == 0):
        return {}
    text = text.lower()
    for c in text:
        if c == ' ':
            continue
        if not c.isalpha():
            text = text.replace(c, '')
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
    for k, v in frequencies.items():
        if isinstance(k, str):
            freq_dict_str_only[k] = v
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
            top_words += freqs_list[i][0],
        return top_words
    for i in range(top_n):
        top_words += freqs_list[i][0],
    return top_words
