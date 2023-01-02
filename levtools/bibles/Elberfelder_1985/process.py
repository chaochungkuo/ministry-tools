import sys
import re
import codecs
import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_verse(conn, verse):
    """
    Create a new task
    :param conn:
    :param verse:
    :return:
    """

    sql = ''' INSERT INTO scriptures(book,ch,verse,text)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, verse)
    conn.commit()

    return cur.lastrowid

def update_scriptures(conn, verse):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param verse:
    :return: verse id
    """
    sql = ''' UPDATE scriptures
              SET text = ? ,
              WHERE book = ? ,
                    ch = ? ,
                    verse = ?'''
    cur = conn.cursor()
    cur.execute(sql, verse)
    conn.commit()

# def main():
database = r"deutsch_bibel.db"

os.remove(database)

sql_create_scriptures_table = """ CREATE TABLE IF NOT EXISTS scriptures (
                                    book integer NOT NULL,
                                    ch integer NOT NULL,
                                    verse integer NOT NULL,
                                    text text NOT NULL
                                ); """
# create a database connection
conn = create_connection(database)
# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_scriptures_table)
else:
    print("Error! cannot create the database connection.")

###########################################

res = []
file_name = "Die_Bibel_Elberfelder_Uebersetzung_Revidiert_1985.txt"

one_ch_books = ["Obadja", "Philemon", "2. Johannes", "3. Johannes", "Judas"]
with codecs.open(file_name, 'r', encoding='cp1252', errors='ignore') as f:
# with open(file_name, encoding='utf-8') as f:
    book_num = 1
    pre_book = None
    for line in f:
        # print(line)
        blocks = line.split("#")
        book, chapter, verse = blocks[1].split(",")
        if book in one_ch_books:
            # print("\t".join([book, chapter, verse]))
            chapter = "0"
        text = blocks[2].replace(verse+".", "")
        text = re.sub(u'-[0-9]*[a-z]*-', '', text)
        text = text.split(" -")[0]
        text = text.strip()
        # print(text)
        # print(text)
        if not pre_book:
            pre_book = book
        elif pre_book != book:
            pre_book = book
            book_num += 1
        
        verse = (book_num, int(chapter), int(verse), text.encode('utf-8').decode('utf-8'))
        # .decode('utf-8')
        # print(verse[3])
        verse_id = create_verse(conn, verse)

        # res.append([book_num, int(chapter), int(verse), text])
        # print(book_num)
        # sys.exit()
# print(len(res))

###########################################
## Update with ReV

# with conn:
#     update_scriptures(conn, (66, 22, 20, "XXX"))