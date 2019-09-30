"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    if isinstance(text, str) == False or text == '' or (text.isalpha() == False and text.count(' ') == 0):
        return {}
    text = text.lower()
    for c in text:
        if c == ' ':
            continue
        if c.isalpha() == False:
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
    if isinstance(frequencies, dict) == False or frequencies == {}:
        return {}
    freq_dict_str_only = {}
    for k, v in frequencies.items():
        if isinstance(k, str):
            freq_dict_str_only[k] = v
    if isinstance(stop_words, tuple) == False:
        return freq_dict_str_only
    for elem in stop_words:
        while elem in freq_dict_str_only:
            del freq_dict_str_only[elem]
    return freq_dict_str_only

def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    if (not isinstance(top_n, int)) or (not isinstance(frequencies, dict)) or (frequencies == {}) or (top_n <= 0):
        return ()
    if top_n >= len(frequencies):
        return frequencies
    freqs_list = list(frequencies.items())
    top_words = ()
    for i in range(top_n):
        top_words += freqs_list[i][0]
    return top_words
