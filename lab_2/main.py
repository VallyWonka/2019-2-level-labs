"""
Labour work #2. Levenstein distance.
"""


def load_from_csv(path_to_file: str) -> list:
    with open(path_to_file) as file:
        edit_matrix = []
        data = file.read().split('\n')
        if '' in data:
            data.remove('')
        for row in data:
            edit_matrix.append(row.split(','))
    return edit_matrix


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if all(isinstance(i, int) for i in [num_rows, num_cols]):
        return [[0 for _ in range(num_cols)] for _ in range(num_rows)]
    return []


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if edit_matrix and all(isinstance(i, int) for i in [add_weight, remove_weight]):
        ind = 1
        for row in edit_matrix[1:]:
            if row:
                edit_matrix[ind][0] = edit_matrix[ind - 1][0] + remove_weight
                ind += 1
        ind = 1
        if edit_matrix[0]:
            for _ in edit_matrix[0][1:]:
                edit_matrix[0][ind] = edit_matrix[0][ind - 1] + add_weight
                ind += 1
    return list(edit_matrix)


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if edit_matrix \
            and all(isinstance(i, int) for i in [add_weight, remove_weight, substitute_weight]) \
            and all(isinstance(i, str) for i in [original_word, target_word]):
        i = 1
        for row in edit_matrix[1:]:
            if len(row) > 1:
                j = 1
                for _ in row[1:]:
                    remove_value = edit_matrix[i - 1][j] + remove_weight
                    add_value = edit_matrix[i][j - 1] + add_weight
                    if original_word[i - 1] != target_word[j - 1]:
                        substitute_value = edit_matrix[i - 1][j - 1] + substitute_weight
                    else:
                        substitute_value = edit_matrix[i - 1][j - 1]
                    row[j] = minimum_value((add_value, remove_value, substitute_value))
                    j += 1
            i += 1
    return list(edit_matrix)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if all(isinstance(i, str) for i in [original_word, target_word]) \
            and all(isinstance(i, int) for i in [add_weight, remove_weight, substitute_weight]):
        return \
            fill_edit_matrix(
                tuple(initialize_edit_matrix(tuple(generate_edit_matrix(len(original_word) + 1, len(target_word) + 1)),
                                             add_weight,
                                             remove_weight)),
                add_weight,
                remove_weight,
                substitute_weight,
                original_word,
                target_word)[-1][-1]
    return -1


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    with open(path_to_file, 'w') as file:
        for row in edit_matrix:
            line = ''
            for col in row:
                line += (str(col) + ',')
            file.write(line[:-1] + '\n')
