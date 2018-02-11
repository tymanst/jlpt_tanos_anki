import genanki
import json
import tempfile


TEST_MODEL = genanki.Model(
  234567, 'foomodel',
  fields=[
    {
      'name': 'AField',
    },
    {
      'name': 'BField',
    },
  ],
  templates=[
    {
      'name': 'card1',
      'qfmt': '{{AField}}',
      'afmt': '{{FrontSide}}'
              '<hr id="answer" style="zoom: 1;">'
              '{{BField}}',
    }
  ],
)

qa_pat = '''<style style="zoom: 1;">.card {{
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}}
</style><span style="font-family: Mincho; font-size: 72px; zoom: 1;">{}</span>
'''



eng_pat = '''<br style="zoom: 1;"><span style="color:#BD6D0B;font-size: 22px; zoom: 1;">{}</span>'''
ru_pat = '''<br style="zoom: 1;"><span style="color:#056859;font-size: 22px; zoom: 1;">{}</span>'''
kun_pat = '''<br style="zoom: 1;"><span style="font-family: Mincho; font-size: 32px; zoom: 1;">{}</span><br style="zoom: 1;">'''
on_pat = '''<br style="zoom: 1;"><span style="font-family: Mincho; color:#585858; font-size: 32px; zoom: 1;">{}</span><br style="zoom: 1;">'''



def load_json(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data

def gen_id(val):
    res = int.from_bytes(str.encode(val), byteorder='little')
    return int(str(res)[:11])


def main():

    deck_name = "KanjiList.N4"
    data = load_json("json/"+ deck_name +".json")
    print(len(data))
    return 0
    deck_name = deck_name + '.tanos-chaos'
    deck = genanki.Deck(gen_id(deck_name), deck_name)
    for el in data:
        question = qa_pat.format(el['kanji'])
        answer = ''
        if 'kun' in el:
            answer += kun_pat.format(el['kun'])
        if 'on' in el:
            answer += on_pat.format(el['on'])
        if 'eng' in el:
            answer += eng_pat.format(el['eng'])
        if 'russian' in el:
            answer += eng_pat.format(el['russian'])
        deck.add_note(genanki.Note(TEST_MODEL, [question, answer]))  # 2 cards
    genanki.Package(deck).write_to_file(deck_name + '.apkg')


if __name__ == '__main__':
    main()