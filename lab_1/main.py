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
