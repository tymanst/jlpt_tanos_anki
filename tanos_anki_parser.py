import json
import os
import re
import unicodedata
from googletrans import Translator
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

def kanji_list_group(file_name):
    array = get_docx_text('docx/' + file_name + '.docx').split('\n')
    array = [i for i in array if i]

    kandji = re.compile(u'[\u4E00-\u9FFF]+')
    hiragana = re.compile(u'[\u3040-\u309Fー]+')
    katakana = re.compile(u'[\u30A0-\u30FF]+')
    result = []
    buffer = {}
    for el in array:
        type = 'eng'
        type = 'on' if katakana.match(el) else type
        type = 'kun' if hiragana.match(el) else type
        type = 'kanji' if kandji.match(el) else type
        if type == 'kanji':
            if 'kanji' in buffer:
                result.append(buffer)
            buffer = {'kanji': el}
        else:
            buffer[type] = el
    return result

def vocab_list_group(file_name):
    array = get_docx_text('docx/' + file_name + '.docx').split('\n')
    array = [i for i in array if i]
    array = array[5:]
    eng_pattern = re.compile(u'[a-zA-Z0-9]+')
    res = []
    buff = []
    for el in array:
        if eng_pattern.match(el):
            try:
                val = {'eng':el}
                val['word'] = buff[0]
                if len(buff) == 2:
                    val['reading'] = buff[1]
                res.append(val)
                buff = []
            except:
                print('Error')
                for el in res:
                    print(el)
                return 0
        else:
            buff.append(el)
    for i, el in enumerate(res):
        res[i]['russian'] = translator.translate(el['word'], dest='ru', src='ja').text
        res[i]['russian_from_eng'] = translator.translate(el['eng'], dest='ru', src='ja').text
    with open('json/' + file_name + '.json', 'w+') as outfile:
        json.dump(res, outfile)
    return len(res)

def vocabList(data):
    for el in data:
        translator = Translator()

    return data
res = 0
for i in range(1,6):
    vocab_list_group('VocabList.N4')


    # for i, el in enumerate(result):
    #     a = os.popen(YARXI_PL + el['kandji']).readline()
    #     if a:
    #         a = a[:a.find(']')]
    #         a = a[a.rfind('[') + 1:]
    #         result[i]['russian'] = a
    #
    # with open('json/' + FILE_NAME + '.json', 'w+') as outfile:
    #     json.dump(result, outfile)
#
#
# print('done ' + FILE_NAME + ' count:' + str(len(result)))