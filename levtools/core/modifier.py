# from collections import OrderedDict
import re
import sys
from levtools.core.scriptures import Scripture, ScriptureSet
from levtools.core.bible import Bible
from docx import Document
from docx.shared import RGBColor
from levtools.core.config import config
from levtools.core.textbody import TextBody

fix_labels = {"EN": {"title": "Title:", "verses": "Scripture Reading:"},
              "DE": {"title": "Thema:", "verses": "Bibelverse:"}}

class Modifier:
    def __init__(self, lang):
        self.lang = lang
        self.lines = []
        self.outline_label = []
        self.bible = Bible(lang=self.lang)
        self.last_book = None
        self.last_chapter = None
        self.last_verse = None
        # self.ref_scriptures = []
        self.second_key = [b[1] for b in list(self.bible.keys.values()) if len(b)>1]
        # self.second_key.remove("of")
        self.en2de_dict = None

    def identify_verses_in_line(self, line, min_words):
        ignore = [".", ",", "(", ")", ";"]
        def hasNumbers(inputString):
            return bool(re.search(r'\d', inputString))
        line = line.replace("—", " ")

        res_scriptures = ScriptureSet(lang=self.lang)

        # print(line)
        for ig in ignore:
            line = line.replace(ig, "")
        l = line.split()

        cont_loop = True
        res = ScriptureSet(lang=self.lang)
        i = 0
        pre_w = ""
        while i < len(l):
            identify_book = False
            w = self.clean_a_word(l[i])
            # print([pre_w, w])
            # print("       " + l[i] + "     "+w)
            ## Define the books
            if " ".join([pre_w, w]) in self.bible.dict.keys():
                self.last_book = self.bible.dict[" ".join([pre_w, w])]
                identify_book = True
            elif w in self.bible.dict.keys():
                self.last_book = self.bible.dict[w]
                identify_book = True
            ## Define reference
            if hasNumbers(w) and not identify_book:
                if 0 < i < len(l) and len(l) > min_words:
                    # print(self.second_key)
                    # print([pre_w, w, l[i+1]])
                    # nextword = " ".join([w, self.clean_a_word(l[i+1])])
                    # print(nextword)
                    if i < len(l)-1 and self.clean_a_word(l[i+1]) in self.second_key:
                    # if i < len(l)-1 and nextword in self.bible.dict.keys():
                        pass
                        # self.process_ref(w, res_scriptures)
                    else:
                        self.process_ref(w, res_scriptures)
            i += 1
            pre_w = w
        return res_scriptures

    # def replace_verses_in_line(self, line, lang1, lang2):
    #     ignore = [".", ",", "(", ")", ";"]
    #     def hasNumbers(inputString):
    #         return bool(re.search(r'\d', inputString))

    #     for ig in ignore:
    #         line = line.replace(ig, "")
    #     l = line.split()

    #     cont_loop = True
    #     res = ScriptureSet(lang=self.lang)
    #     i = 0
    #     pre_w = ""
    #     while i < len(l):
    #         res_scriptures = ScriptureSet(lang=lang1)
    #         identify_book = False
    #         w = self.clean_a_word(l[i])

    #         if " ".join([pre_w, w]) in self.bible.dict.keys():
    #             self.last_book = self.bible.dict[" ".join([pre_w, w])]
    #             identify_book = True
    #         elif w in self.bible.dict.keys():
    #             self.last_book = self.bible.dict[w]
    #             identify_book = True
    #         ## Define reference
    #         if hasNumbers(w) and not identify_book:
    #             if i < len(l):
    #                 if i < len(l)-1 and self.clean_a_word(l[i+1]) in self.second_key:
    #                     self.process_ref(w, res_scriptures)
    #                 else:
    #                     self.process_ref(w, res_scriptures)
    #         # replace scrip in line
    #         i += 1
    #         pre_w = w
    #     return res_scriptures

    def identify_scriptures(self, textbody, min_words=1):
        textbody.scriptures = []
        for i, line in enumerate(textbody.texts):
            ref = self.identify_verses_in_line(line, min_words)
            textbody.scriptures.append(ref)
    
    def print_scriptures(self, textbody, with_text=False):
        textbody.scriptures_str = []
        for i, ref in enumerate(textbody.scriptures):
            if not with_text:
                textbody.scriptures_str.append(ref.print_each(self.bible))
            else:
                textbody.scriptures_str.append(ref.print_each_with_text(self.bible))

    def clean_a_word(self, word):
        a = [";", "(", ")", "\xe2","\x80","\x9c", "\x9d", ".", ",", "\x99",
             "\x94", " ", "\x93", "\x80\x9c", "\xa0"]
        for aa in a:
            if aa in word:
                word = word.replace(aa, "")
        if re.match(r'[0-9]*[a,b]', word):
            word = re.sub('\D', '', word)
        return word

    def process_ref(self, ref, res):
        def clean_vv(w):
        # Clean the format of the verses
            if ";" in w:
                w = w.replace(";", "")
            w = re.sub(r'[a-z]+', '', w, re.I)
            return w

        def handle_verses(v):
            v = clean_vv(v)
            # print(v)
            try:
                if "-" in v:
                    l = v.split("-")
                    return list(range(int(l[0]), int(l[1])+1))
                elif "–" in v:
                    l = v.split("–")
                    return list(range(int(l[0]), int(l[1])+1))
                else:
                    return [int(v)]
            except:
                print("************ Loading verse fails: "+v)

        def distribute_verses(vv, res):
            try:
                for v in vv:
                    res.add(Scripture(self.last_book, self.last_chapter, v))
            except:
                pass

        # print(w)
        ref = re.sub(':$', '', ref)
        if ":" in ref:
            ww = ref.rstrip("a").rstrip("b").split(":")
            try:
                self.last_chapter = int(ww[0])
                vv = handle_verses(ww[1])
                distribute_verses(vv, res)
            except:
                print("Cannot read: "+ww[0])
            
        else:
            vv = handle_verses(ref)
            distribute_verses(vv, res)

    def setup_en2de(self):
        mod_en = Modifier(lang="EN")
        text_en = TextBody(config["EN"]["en2de"])
        mod_en.identify_scriptures(text_en, min_words=0)

        mod_de = Modifier(lang="EN")
        text_de = TextBody(config["DE"]["en2de"])
        mod_de.identify_scriptures(text_de, min_words=0)
        # print(len(text_de.scriptures))

        self.en2de_dict = {}
        for i, ref in enumerate(text_en.scriptures):
            if ref:
                self.en2de_dict[str(ref[0])] = text_de.scriptures[i][0]
    
    def convert_en2de(self, textbody):
        if not self.en2de_dict:
            self.setup_en2de()
            self.bible = Bible(lang="DE")
        # parse each verse
        for i, ref in enumerate(textbody.scriptures):
            for j, v in enumerate(ref):
                if str(v) in self.en2de_dict.keys():
                    # print([str(textbody.scriptures[i][j]), str(self.en2de_dict[str(v)])])
                    textbody.scriptures[i][j] = self.en2de_dict[str(v)]
                    # print(str(textbody.scriptures[i][j]))
            textbody.scriptures[i].lang = "DE"

    def add_de_lines(self, textbody):
        textbody.de_lines = []
        for i, text in enumerate(textbody.texts):
            de = []
            if "Scripture Reading" in text:
                de.append("Bibelverse:")
            if "“" in text:
                de.append("„")
            if "”" in text:
                de.append("“")
            if "—" in text:
                de.append("–")
            if " vv." in text:
                de.append("V.")
            if " v." in text:
                de.append("V.")
            if textbody.scriptures[i]:
                de.append(textbody.scriptures[i].print_combined_ref(self.bible))
            if len(text) > 0 and text[-1] in [":", "."]:
                de.append(text[-1])
            if not de:
                de.append("[DE]")
            textbody.de_lines.append(" ".join(de))

