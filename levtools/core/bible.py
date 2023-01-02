import io
import os
import configparser
import pickle
from flask import current_app
from levtools.core.config import config


class Bible:
    def __init__(self, lang):
        self.lang = lang
        self.dict = {}
        self.keys = {}
        self.output = {}
        self.load_books(lang)
        self.get_output(lang)
        self.en2de_dict = {}

    def load_books(self, lang):
        def load_f(f):
            for line in f:
                l = line.strip().split(";")
                self.dict[l[0]] = int(l[1])
                self.keys[l[0]] = l[0].split()

        if lang == "EN":
            # with io.open("./config/EN_Books.csv", mode="r", encoding="utf-8") as f:
            with io.open(config['EN']['book_names'], encoding="utf-8") as f:
                load_f(f)
        elif lang == "DE":
            # with io.open("./config/EN_Books.csv", mode="r", encoding="utf-8") as f:
            with io.open(config['DE']['book_names'], encoding="utf-8") as f:
                load_f(f)

    def get_key(self, ind, filter):
        res = []
        if ind == 0:
            for k, v in self.keys.items():
                res.append([v[ind], self.dict[k]])
        else:
            for k, v in self.keys.items():
                if ind < len(v) and self.dict[k] in filter:
                    res.append([v[ind], self.dict[k]])
        return res

    def get_output(self, lang):
        if lang == "EN":
            outfile = config['EN']['book_output']
        elif lang == "DE":
            outfile = config['DE']['book_output']

        with io.open(outfile, encoding="utf-8") as f:
            for line in f:
                l = line.strip().split(";")
                self.output[int(l[1])] = l[0]
