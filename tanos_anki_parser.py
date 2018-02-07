import json
import os
import re
import unicodedata
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

from googletrans import Translator

FILE_NAME = 'KanjiList.N5'
YARXI_PL = 'perl \'' + os.getcwd() + '/yarxi-pl/yarxi.pl\' '

translator = Translator()

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

array = get_docx_text('docx/' + FILE_NAME + '.docx').split('\n')
array = [i for i in array if i]

kandji = re.compile(u'[\u4E00-\u9FFF]+')
hiragana = re.compile(u'[\u3040-\u309Fー]+')
katakana = re.compile(u'[\u30A0-\u30FF]+')
result = []
buffer = {}
for el in array:
    type = 'eng'
    type = 'katakana' if katakana.match(el) else type
    type = 'hiragana' if hiragana.match(el) else type
    type = 'kandji' if kandji.match(el) else type
    if type == 'kandji':
        if 'kandji' in buffer:
            result.append(buffer)
        buffer = {'kandji': el}
    else:
        buffer[type] = el


for i, el in enumerate(result):
    a = os.popen(YARXI_PL + el['kandji']).readline()
    if a:
        a = a[:a.find(']')]
        a = a[a.rfind('[') + 1:]
        result[i]['russian'] = a

with open('json/' + FILE_NAME + '.json', 'w+') as outfile:
    json.dump(result, outfile)
print('done')

print('done ' + FILE_NAME + ' count:' + str(len(result)))