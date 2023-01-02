import sys
sys.path.insert(0,'/Users/ckuo/github/ministry_tools')
from levtools.core.textbody import TextBody
from levtools.core.modifier import Modifier

# mod = Modifier("DE")
# inputfile = TextBody(path="Overcomers_ch1.docx", format="book")
# mod.identify_scriptures(inputfile)
# mod.print_scriptures(inputfile, with_text=True)
# inputfile.save_docx("output1.docx", ref=True)


mod = Modifier("EN")
inputfile = TextBody(path="21ITERO-S01.docx", format="book")
mod.identify_scriptures(inputfile)
# print(len(inputfile.scriptures))
# print(str(inputfile.scriptures[3][0]))

mod.convert_en2de(inputfile)
mod.add_de_lines(inputfile)
mod.print_scriptures(inputfile, with_text=True)
inputfile.save_docx("output2.docx", ref=True, de=True)

# inputfile = TextBody(path="EN_outline.txt", format="book")
# print(inputfile.path)
# print(inputfile.ext)
# print(inputfile.format)
# print(inputfile.texts[0:5])

# from lev_app.core.config import config
