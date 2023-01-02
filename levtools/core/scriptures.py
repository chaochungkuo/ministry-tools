import sqlite3
from sqlite3 import Error
from levtools.core.config import config

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def get_verse(conn, book, ch, v):
    """
    Query tasks by scripture
    :param conn: the Connection object
    :param scripture:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM scriptures WHERE book=? AND ch=? AND verse=? ", (book, ch, v))

    rows = cur.fetchall()
    if rows:
        tt = rows[0][3].encode().decode()
    else:
        tt = None
    return tt

class Scripture:
    def __init__(self, book_index, chapter, verse):
        if book_index is None: book_index = 0
        if chapter is None: chapter = 0
        if verse is None: verse = 0
        self.code = [book_index, chapter, verse]
    def __hash__(self):
        return hash(tuple(self.code))
    def __getitem__(self, key):
        return self.code[key]
    def __eq__(self, other):
        return self.code == other.code
    def __cmp__(self, other):
       """Return negative value if x < y, zero if x == y and strictly positive if x > y."""
       if self.code[0] < other.code[0]:
           return -1
       elif self.code[0] > other.code[0]:
           return 1
       else:
           if self.code[1] < other.code[1]:
               return -1
           elif self.code[1] > other.code[1]:
               return 1
           else:
               if self.code[2] < other.code[2]:
                   return -1
               elif self.code[2] > other.code[2]:
                   return 1
               else:
                   return 0
    def __lt__(self, other):
        return self.__cmp__(other) < 0
    def __gt__(self, other):
        return self.__cmp__(other) > 0
    def __eq__(self, other):
        return self.__cmp__(other) == 0
    def __le__(self, other):
        return self.__cmp__(other) <= 0
    def __ge__(self, other):
        return self.__cmp__(other) >= 0
    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __str__(self):
        return "-".join([str(x) for x in self.code if x > 0])

    def getnext(self):
        res = self.code.copy()
        res[2] += 1
        return res


class ScriptureSet:
    def __init__(self, lang, convert_en2de=False):
        self.list = []
        self.lang = lang
        # self.convert_en2de_dict = {}
        # if convert_en2de:
        #     self.convert_en2de()

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, value):
        self.list[key] = value

    def add(self, ref):
        self.list.append(ref)


    def print_each(self, bible):
        res = []
        for s in self.list:
            if s[1] == 0:
                res.append(bible.output[s[0]] + " "+str(s[2]))
            else:
                res.append(bible.output[s[0]] + " " + str(s[1])+":"+str(s[2]))
        return ", ".join(res)

    def print_each_with_text(self, bible):
        # print(config["deutschbibel"])
        conn = create_connection(config["deutschbibel"])
        res = []
        for s in self.list:
            if s[0] == 0:
                continue
            elif s[1] == 0:
                ref = bible.output[s[0]] + " "+str(s[2])
            else:
                ref = bible.output[s[0]] + " " + str(s[1])+":"+str(s[2])
            tt = get_verse(conn, s[0], s[1], s[2])
            # print(tt)
            if tt:
                ref = '{0: <15}'.format(ref)
                res.append(ref + tt)
            else:
                continue
        return "\n".join(res)


    def print_line(self, bible):
        for s in self.list:
            if s[1] == 0:
                print(bible.output[s[0]] + " " +str(s[2]))
            else:
                print(bible.output[s[0]] + " " + str(s[1])+":"+str(s[2]))

    def print_combined_ref(self, bible):
        def ref(s):
            if s[1] == 0:
                res = bible.output[s[0]] + " "+str(s[2])
            else:
                res = bible.output[s[0]] + " " + str(s[1])+":"+str(s[2])
            return res
        
        if len(self) > 0:

            res = []
            pair1 = None
            # pair2 = None
            cont = False
            for i, s in enumerate(self.list):
                # print(ref(s))
                # print(self.list[i+1])
                if i < len(self) - 1:
                    if s.getnext() == self.list[i+1].code:
                        if not cont:
                            cont = True
                            pair1 = s
                        else:
                            continue
                    else:
                        if cont and pair1:
                            res.append(ref(pair1)+"–"+str(s[2]))
                            pair1 = None
                            cont = False
                        else:
                            res.append(ref(s))
                else:
                    if cont and pair1:
                        res.append(ref(pair1)+"–"+str(s[2]))
                    else:
                        res.append(ref(s))
            # print("; ".join(res))
            return "; ".join(res)
        else:
            return ""

