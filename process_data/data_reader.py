import numpy as np
import os
import random
from collections import Counter

import constants as c


class DataReader:
    def __init__(self, artist_name):
        self.artist = artist_name
        self.lyrics = []
        self.lyric_indices = []
        self.vocab_lookup = {}

    def get_path(self):
        return os.path.join('../data/artists/', self.artist)

    def load_lyrics(self):
        path = self.get_path()
        for fn in os.listdir(path):
            with open(os.path.join(path, fn), 'r') as song:
                song_lyrics = self.clean_string(song.read()).split()
                self.lyrics.append(song_lyrics)

    def get_vocab(self):
        if len(self.lyrics) == 0:
            self.load_lyrics()

        all_words = reduce(lambda a, b: a + b, self.lyrics)

        tokens = sorted(list(set(all_words)))

        self.vocab_lookup = dict((word, i) for i, word in enumerate(tokens))
        self.lyric_indices = [map(lambda word: self.vocab_lookup[word], song)
                              for song in self.lyrics]

        print len(tokens)

        return tokens

    def get_train_batch(self, batch_size, seq_len):
        inputs = np.empty([batch_size, seq_len], dtype=int)
        targets = np.empty([batch_size, seq_len], dtype=int)

        for i in xrange(batch_size):
            inp, target = self.get_seq(seq_len)
            inputs[i] = inp
            targets[i] = target

        return inputs, targets

    def get_seq(self, seq_len):
        for i in xrange(1000):
            song = random.choice(self.lyric_indices)
            if len(song) > seq_len:
                break

        i = random.randint(0, len(song) - (seq_len + 1))
        inp = np.array(song[i:i + seq_len], dtype=int)
        target = np.array(song[i + 1:i + seq_len + 1], dtype=int)
        return inp, target

    def clean_string(self, string):
        string = string.lower()

        clean_words = []
        for word in string.split():
            if word[0] == '"' and word[-1] != '"':
                word = word[1:]
            elif word[-1] == '"' and word[0] != '"':
                word = word[-1]

            if word[0] == '(' and word[-1] != ')':
                word = word[1:]
            elif word[-1] == ')' and word[0] != '(':
                word = word[:-1]

            clean_words.append(word)

        return ' '.join(clean_words)
