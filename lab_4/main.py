import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    corpus = []
    if isinstance(texts, list):
        texts = [text for text in texts if (text and isinstance(text, str))]
        for text in texts:
            text = text.lower()
            for char in text:
                text = text.replace('<br />', ' ')
                if not char.isalpha() and char != ' ':
                    text = text.replace(char, '')
            corpus.append(text.split())
    return corpus


class TfIdfCalculator:
    def __init__(self, corpus=[]):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = []

    def calculate_tf(self):
        if self.corpus:
            texts = [text for text in self.corpus if (text and isinstance(text, list))]
            for text in texts:
                text_values = {}
                text = [word for word in text if isinstance(word, str)]
                for word in text:
                    if word not in text_values:
                        text_values[word] = text.count(word) / len(text)
                self.tf_values.append(text_values)
        return self.tf_values

    def calculate_idf(self):
        if self.corpus:
            texts = [text for text in self.corpus if (text and isinstance(text, list))]
            for text in texts:
                text = [word for word in text if isinstance(word, str)]
                for word in text:
                    if word not in self.idf_values:
                        docs = [doc for doc in texts if word in doc]
                        self.idf_values[word] = math.log(len(texts) / len(docs))
        return self.idf_values

    def calculate(self):
        if self.tf_values and self.idf_values:
            for ind, text in enumerate(self.tf_values):
                text_tf_idf = {}
                for word in text.keys():
                    if word not in text_tf_idf:
                        text_tf_idf[word] = self.tf_values[ind][word] * self.idf_values[word]
                self.tf_idf_values.append(text_tf_idf)
        return self.tf_idf_values

    def report_on(self, word, document_index):
        try:
            value = self.tf_idf_values[document_index][word]
        except (TypeError, IndexError, KeyError):
            return ()
        sorted_by_tfidf = sorted(self.tf_idf_values[document_index].items(), key=lambda x: -x[1])
        rating = [array[0] for array in sorted_by_tfidf].index(word)
        return value, rating

    def dump_report_csv(self):
        if self.tf_idf_values:
            tfs = ['TF ({})'.format(file) for file in self.file_names]
            tfs = ','.join(tfs)
            tf_idfs = ['TF-IDF ({})'.format(file) for file in self.file_names]
            tf_idfs = ','.join(tf_idfs)
            head = 'Word,' + tfs + ',IDF,' + tf_idfs + '\n'
            words = []
            for text in self.corpus:
                for word in text:
                    if word not in words:
                        words.append(word)
            file_lines = []
            for word in words:
                file_list = [word]
                for text in self.tf_values:
                    if word in text:
                        file_list.append(str(text[word]))
                    else:
                        file_list.append('0')
                file_list.append(str(self.idf_values[word]))
                for text in self.tf_idf_values:
                    if word in text:
                        file_list.append(str(text[word]))
                    else:
                        file_list.append('0')
                file_line = ','.join(file_list)
                file_lines.append(file_line + '\n')
        with open('report.csv', 'w') as file:
            file.write(head)
            file.writelines(file_lines)

    def cosine_distance(self, index_text_1, index_text_2):
        try:
            text_1 = self.corpus[index_text_1]
            text_2 = self.corpus[index_text_2]
        except IndexError:
            return 1000
        words = []
        both_texts = text_1 + text_2
        for word in both_texts:
            if word not in words:
                words.append(word)
        encoded_1 = []
        encoded_2 = []
        for word in words:
            if word in text_1:
                encoded_1.append(self.tf_idf_values[index_text_1][word])
            elif word not in text_1:
                encoded_1.append(0)
            if word in text_2:
                encoded_2.append(self.tf_idf_values[index_text_2][word])
            elif word not in text_2:
                encoded_2.append(0)
        iterations = len(encoded_1)
        dot_product = sum([encoded_1[i] * encoded_2[i] for i in range(iterations)])
        length_1 = math.sqrt(sum([encoded_1[i] ** 2 for i in range(iterations)]))
        length_2 = math.sqrt(sum([encoded_2[i] ** 2 for i in range(iterations)]))
        cosine_distance = dot_product / (length_1 * length_2)
        return cosine_distance



if __name__ == '__main__':
    tf_idf = TfIdfCalculator()
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
            tf_idf.file_names.append(text)
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf.corpus = test_texts
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
