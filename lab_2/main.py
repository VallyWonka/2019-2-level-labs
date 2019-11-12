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

            
def describe_edits(edit_matrix: tuple,
                   original_word: str,
                   target_word: str) -> list:
    steps = []
    if all(char not in list(target_word) for char in list(original_word)):
        if len(original_word) > len(target_word):
            steps = ['substitute {} with {}'.format(x, y) for x, y in
                     zip(list(original_word[:len(target_word)]), list(target_word))] \
                    + ['remove {}'.format(x) for x in list(original_word[len(target_word):])]
        else:
            steps = ['substitute {} with {}'.format(x, y) for x, y in
                     zip(list(original_word), list(target_word[:len(original_word)]))] \
                    + ['insert {}'.format(x) for x in list(target_word[len(original_word):])]
    else:
        # find common strings
        common_chars_row = ''
        row_indices = []
        for ind, elem in enumerate(edit_matrix[-1][1:]):
            if elem < edit_matrix[-1][ind]:
                common_chars_row += target_word[ind]
                row_indices.append(ind)
        last_col = [row[-1] for row in edit_matrix]
        common_chars_col = ''
        col_indices = []
        for ind, elem in enumerate(last_col[1:]):
            if elem < last_col[ind]:
                common_chars_col += original_word[ind]
                col_indices.append(ind)
        # check validity
        common_possibilities = [common_chars_row, common_chars_col]
        indices = [row_indices, col_indices]
        original_word_temp = original_word
        for char in original_word:
            if char not in common_chars_row:
                original_word_temp = original_word_temp.replace(char, '')
        if common_chars_row not in original_word_temp:
            common_possibilities.remove(common_chars_row)
            indices.remove(row_indices)
        target_word_temp = target_word
        for char in target_word:
            if char not in common_chars_col:
                target_word_temp = target_word_temp.replace(char, '')
        if common_chars_col not in target_word_temp:
            common_possibilities.remove(common_chars_col)
            indices.remove(col_indices)
        # forming descriptions list
        if common_chars_row in common_possibilities:
            # before common strings
            beginning_targ = target_word[:indices[0][0]]
            beginning_orig = original_word[:original_word.find(common_chars_row[0])]
            if beginning_targ and beginning_orig:
                if len(beginning_targ) > len(beginning_orig):
                    actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(beginning_orig, beginning_targ[:len(beginning_orig)])]
                    actions_targ = ['insert {}'.format(char) for char in beginning_targ[len(beginning_orig):]]
                    steps += actions_orig + actions_targ
                else:
                    actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(beginning_orig[:len(beginning_targ)], beginning_targ)]
                    actions_orig = ['remove {}'.format(char) for char in beginning_orig[len(beginning_targ):]]
                    steps += actions_targ + actions_orig
            elif beginning_targ:
                steps += ['insert {}'.format(char) for char in beginning_targ]
            elif beginning_orig:
                steps += ['remove {}'.format(char) for char in beginning_orig]
            # inside common strings
            for ind, char in enumerate(common_chars_row[:-1], 1):
                inside_orig = original_word[original_word.find(char) + 1:original_word.find(common_chars_row[ind])]
                inside_targ = target_word[target_word.find(char) + 1:target_word.find(common_chars_row[ind])]
                if inside_orig and inside_targ:
                    if len(inside_targ) > len(inside_orig):
                        actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                        zip(inside_orig, inside_targ[:len(inside_orig)])]
                        actions_targ = ['insert {}'.format(char) for char in inside_targ[len(inside_orig):]]
                        steps += actions_orig + actions_targ
                    else:
                        actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                        zip(inside_orig[:len(inside_targ)], inside_targ)]
                        actions_orig = ['remove {}'.format(char) for char in inside_orig[len(inside_targ):]]
                        steps += actions_targ + actions_orig
                elif inside_orig:
                    steps += ['remove {}'.format(char) for char in inside_orig]
                elif inside_targ:
                    steps += ['insert {}'.format(char) for char in inside_targ]
            # ends of words
            remaining_targ = target_word[indices[0][-1] + 1:]
            remaining_orig = original_word[:original_word.find(common_chars_row[-1]):-1]
            if remaining_targ and remaining_orig:
                if len(remaining_targ) > len(remaining_orig):
                    actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(remaining_orig[::-1], remaining_targ[:len(remaining_orig)])]
                    actions_targ = ['insert {}'.format(char) for char in remaining_targ[len(remaining_orig):]]
                    steps += actions_orig + actions_targ
                else:
                    actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(remaining_orig[:len(remaining_targ)][::-1], remaining_targ)]
                    actions_orig = ['remove {}'.format(char) for char in remaining_orig[len(remaining_targ):]]
                    steps += actions_targ + actions_orig
            elif remaining_targ:
                steps += ['insert {}'.format(char) for char in remaining_targ]
            elif remaining_orig:
                steps += ['remove {}'.format(char) for char in remaining_orig[::-1]]
        if common_chars_col in common_possibilities:
            # before common strings
            steps_2 = []
            beginning_targ = target_word[:target_word.find(common_chars_col[0])]
            beginning_orig = original_word[:indices[-1][0]]
            if beginning_targ and beginning_orig:
                if len(beginning_targ) > len(beginning_orig):
                    actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(beginning_orig, beginning_targ[:len(beginning_orig)])]
                    actions_targ = ['insert {}'.format(char) for char in beginning_targ[len(beginning_orig):]]
                    steps_2 += actions_orig + actions_targ
                else:
                    actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(beginning_orig[:len(beginning_targ)], beginning_targ)]
                    actions_orig = ['remove {}'.format(char) for char in beginning_orig[len(beginning_targ):]]
                    steps_2 += actions_targ + actions_orig
            elif beginning_targ:
                steps_2 += ['insert {}'.format(char) for char in beginning_targ]
            elif beginning_orig:
                steps_2 += ['remove {}'.format(char) for char in beginning_orig]
            # inside common strings
            for ind, char in enumerate(common_chars_col[:-1], 1):
                inside_orig = original_word[original_word.find(char) + 1:original_word.find(common_chars_col[ind])]
                inside_targ = target_word[target_word.find(char) + 1:target_word.find(common_chars_col[ind])]
                if inside_orig and inside_targ:
                    if len(inside_targ) > len(inside_orig):
                        actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                        zip(inside_orig, inside_targ[:len(inside_orig)])]
                        actions_targ = ['insert {}'.format(char) for char in inside_targ[len(inside_orig):]]
                        steps_2 += actions_orig + actions_targ
                    else:
                        actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                        zip(inside_orig[:len(inside_targ)], inside_targ)]
                        actions_orig = ['remove {}'.format(char) for char in inside_orig[len(inside_targ):]]
                        steps_2 += actions_targ + actions_orig
                elif inside_orig:
                    steps_2 += ['remove {}'.format(char) for char in inside_orig]
                elif inside_targ:
                    steps_2 += ['insert {}'.format(char) for char in inside_targ]
                    print(inside_targ, 'I am here')
            # ends of words
            remaining_targ = target_word[::-1][:target_word[::-1].find(common_chars_col[-1])]
            remaining_orig = original_word[indices[-1][-1] + 1:]
            if remaining_targ and remaining_orig:
                if len(remaining_targ) > len(remaining_orig):
                    actions_orig = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(remaining_orig[::-1], remaining_targ[:len(remaining_orig)])]
                    actions_targ = ['insert {}'.format(char) for char in remaining_targ[len(remaining_orig):]]
                    steps_2 += actions_orig + actions_targ
                else:
                    actions_targ = ['substitute {} with {}'.format(x, y) for x, y in
                                    zip(remaining_orig[:len(remaining_targ)][::-1], remaining_targ)]
                    actions_orig = ['remove {}'.format(char) for char in remaining_orig[len(remaining_targ):]]
                    steps_2 += actions_targ + actions_orig
            elif remaining_targ:
                steps_2 += ['insert {}'.format(char) for char in remaining_targ]
            elif remaining_orig:
                steps_2 += ['remove {}'.format(char) for char in remaining_orig]
    if steps and steps_2:
        steps = sorted([steps, steps_2], key=len)[0]
    elif steps_2:
        steps = steps_2
    return steps
