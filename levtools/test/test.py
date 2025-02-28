import sys
import os
sys.path.insert(0,'/Users/jovesus/github/ministry-tools')
from levtools.core.textbody import TextBody
from levtools.core.modifier import Modifier

directory = "./2024_thanksgiving"
for filename in os.listdir(directory):
    # Check if the file ends with '.docx'
    if filename.endswith('.docx'):
        file_path = os.path.join(directory, filename)
        file_name = os.path.basename(filename).split(".")[0]
        print(file_name)
        mod = Modifier("DE")
        inputfile = TextBody(path=file_path, format="book")
        mod.identify_scriptures(inputfile)
        # print("1")
        mod.print_scriptures(inputfile, with_text=True)
        inputfile.save_docx(filename, ref=True)


# mod = Modifier("EN")
# inputfile = TextBody(path="21ITERO-S01.docx", format="book")
# mod.identify_scriptures(inputfile)
# print(len(inputfile.scriptures))
# print(str(inputfile.scriptures[3][0]))

# mod.convert_en2de(inputfile)
# mod.add_de_lines(inputfile)
# mod.print_scriptures(inputfile, with_text=True)
# inputfile.save_docx("output2.docx", ref=True, de=True)

# inputfile = TextBody(path="EN_outline.txt", format="book")
# print(inputfile.path)
# print(inputfile.ext)
# print(inputfile.format)
# print(inputfile.texts[0:5])

# from lev_app.core.config import config
