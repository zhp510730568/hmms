import os
from collections import Counter

data_path='../data'

pos_dict_name='pos'


class HmmParams():
    def __init__(self, pos_dict_path=None, corpus_path=None):
        if pos_dict_path is None:
            raise ValueError('pos_dict_path must not be None')
        if corpus_path is None:
            raise ValueError('corpus_path must not be None')
        self.pos_dict_path=pos_dict_path
        self._load_pos_dict()

        self.corpus_path=corpus_path
        self.total_count = 0
        self._load_corpus()

    def _load_pos_dict(self):
        self.pos_dict = Counter()
        with open(self.pos_dict_path, 'r') as f:
            for pos in f:
                arr = pos.split()
                self.pos_dict[arr[0]]=0

    def _load_corpus(self):
        print('pos_dict: ', self.pos_dict)
        corpus_files = os.listdir(self.corpus_path)
        for corpus_name in corpus_files:
            with open(os.path.join(self.corpus_path, corpus_name), 'r') as f:
                for line in f:
                    arr = line.split('\t ', 2)
                    if len(arr) == 2:
                        sentence = arr[1].strip()
                        words, tags=self.get_word_and_pos(sentence)
                        previous=''
                        for index in range(len(words)):
                            if index == 0:
                                previous = tags[0]
                                if previous in self.pos_dict:
                                    self.pos_dict[previous] += 1
                                self.total_count += 1
                            else:
                                current=tags[index]
        total = 0
        for key, value in self.pos_dict.items():
            self.pos_dict[key] = value / self.total_count
            total += value / self.total_count
            print(key, self.pos_dict[key])
        print(total)

    def get_word_and_pos(self, sentence):
        '''
        get words and tags from sentence
        :param sentence:
        :return:
        '''
        word = ''
        pos = ''
        is_pos = False
        words = []
        tags = []
        for ch in sentence:
            if ch.isspace():
                if word.strip() != '' and pos.strip() != '':
                    words.append(word.strip())
                    tags.append(pos.strip())
                    word = ''
                    pos = ''
                    is_pos = False
            elif ch == '/':
                is_pos = True
                pos = ''
            else:
                if not is_pos:
                    word += ch
                else:
                    pos += ch
        if word != '' and pos != '':
            words.append(word)
            tags.append(pos)
        return words, tags


if __name__=='__main__':
    params=HmmParams(os.path.join(data_path, pos_dict_name), os.path.join(data_path, 'corpus'))