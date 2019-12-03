"""
Labour work #3
Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if isinstance(word, str) and word not in self.storage:
            id_num = list(self.storage.values())[-1] + 1 if self.storage else 0
            self.storage[word] = id_num
            return id_num

    def get_id_of(self, word: str) -> int:
        if isinstance(word, str) and word in self.storage:
            return self.storage[word]
        return -1

    def get_original_by(self, id_num: int) -> str:
        ids = list(self.storage.values())
        words = list(self.storage.keys())
        if isinstance(id_num, int) and id_num in ids:
            index = ids.index(id_num)
            return words[index]
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if corpus and isinstance(corpus, tuple):
            for item in corpus:
                if isinstance(item, list):
                    for word in item:
                        self.put(word)
                else:
                    self.put(item)


class NGramTrie:
    def __init__(self, N=2):
        self.size = N
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> dict:
        if sentence and isinstance(sentence, tuple):
            for ind, elem in enumerate(sentence[:-(self.size - 1)]):
                prefix = (elem, ) + sentence[ind + 1:ind + self.size]
                if prefix in self.gram_frequencies:
                    self.gram_frequencies[prefix] += 1
                else:
                    self.gram_frequencies[prefix] = 1
        return self.gram_frequencies

    def calculate_log_probabilities(self):
        combinations = list(self.gram_frequencies.keys())
        for combination in combinations:
            if combination not in self.gram_log_probabilities:
                prefix = combination[:-1]
                prefix_values = [self.gram_frequencies[gram] for gram in self.gram_frequencies if gram[:-1] == prefix]
                log_probability = math.log((self.gram_frequencies[combination] / sum(prefix_values)))
                self.gram_log_probabilities[combination] = log_probability
        return self.gram_log_probabilities

    def predict_next_sentence(self, prefix: tuple) -> list:
        sentence = []
        if prefix and isinstance(prefix, tuple) and self.size == len(prefix) + 1:
            sentence.extend(prefix)
            grams = list(self.gram_log_probabilities.keys())
            prefixes = [gram[:-1] for gram in grams]
            while prefix in prefixes:
                with_prefix = [gram for gram in grams if gram[0] == prefix[0]]
                values = [value for key, value in self.gram_log_probabilities.items() if key in with_prefix]
                ind = values.index(max(values))
                sentence.append(with_prefix[ind][-1])
                prefix = tuple(sentence[-(self.size - 1):])
        return sentence


def encode(storage_instance, corpus) -> list:
    for sentence in corpus:
        for ind, word in enumerate(sentence):
            if word in storage_instance.storage:
                sentence[ind] = storage_instance.storage[word]
            else:
                storage_instance.put(word)
                sentence[ind] = storage_instance.storage[word]
    return corpus


def split_by_sentence(text: str) -> list:
    if not isinstance(text, str):
        return []
    text = text.replace('\n', ' ')
    for char in text:
        if char == ' ':
            continue
        if not char.isalpha() and char not in ".!?":
            text = text.replace(char, '')
    if all(symbol not in text for symbol in ' .!?'):  # redo the check although works
        return []
    sentences = []
    counter = 0
    for ind, char in enumerate(text[3:]):
        if char.upper() and text[ind + 2] == ' ' and text[ind + 1] in '.!?':
            sentences.append(text[counter:ind + 1])
            counter = ind + 3
        elif ind == len(text[3:]) - 1:
            sentences.append(text[counter:-1])
    result = []
    for sentence in sentences:
        sentence = '<s> ' + sentence + ' </s>'
        result.append(sentence.lower().split())
    return result
