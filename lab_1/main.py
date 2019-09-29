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
        if c.isalpha() == False:
            text = text.replace(c, ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
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
    return 'hello. it IS me'

def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    pass
