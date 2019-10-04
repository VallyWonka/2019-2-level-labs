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


# PATH_TO_FILE = 'C:\\data.txt'
# LINES_LIMIT = 5
# print(read_from_file(PATH_TO_FILE, LINES_LIMIT))


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
    top_words = ()
    if len(frequencies) > 0 and top_n > 0:
        freqs_list = list(frequencies.items())
        if top_n >= len(frequencies):
            for i in range(len(frequencies)):
                top_words += (freqs_list[i][0],)
        else:
            for i in range(top_n):
                top_words += (freqs_list[i][0],)
    return top_words


def write_to_file(path_to_file: str, content: tuple):
    if isinstance(path_to_file, str) and isinstance(content, tuple):
        with open(path_to_file, 'w') as file:
            for elem in content:
                elem += '\n'
                file.write(elem)


# def create_content(freqs_dict: dict):
    # content = ()
    # list_of_words = list(freqs_dict.items())
    # list_of_words.sort(key=lambda i: i[1], reverse=True)
    # for elem in list_of_words:
        # content += (elem[0], )
    # return content


# PATH_TO_FILE = 'C:\\report.txt'
# FREQS_DICT = calculate_frequences('''
# Als ich noch ein Knabe war,
# Sperrte man mich ein;
# Und so sass ich manches Jahr
# Ueber mir allein,
# Wie in Mutterleib.

# Doch du warst mein Zeitvertreib,
# Goldne Phantasie.
# Und ich ward ein warmer Held,
# Wie der Prinz Pipi,
# Und durchzog die Welt.''')


# CONTENT = create_content(FREQS_DICT)
# write_to_file(PATH_TO_FILE, CONTENT)
