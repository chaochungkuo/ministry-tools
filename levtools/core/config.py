from os.path import join, dirname, realpath

my_path = dirname(dirname(realpath(__file__)))
config = {"EN": {"book_names": join(my_path,'data/books/EN_Books.csv'),
                 "book_output": join(my_path,'data/books/EN_Books_output.csv'),
                 "en2de": join(my_path,'data/en2de/en.txt')},
          "DE": {"book_names": join(my_path,'data/books/DE_Books.csv'),
                 "book_output": join(my_path,'data/books/DE_Books_output.csv'),
                 "en2de": join(my_path,'data/en2de/de.txt')},
          "en2de_convertor": join(my_path,'data/en2de/en2de.convertor.pickle'),
          "deutschbibel": join(my_path,'bibles/deutsch_bibel.db')}

# en_file = os.path.join(my_path,'data/en2de/en.txt')
# de_file = os.path.join(my_path,'data/en2de/de.txt')
