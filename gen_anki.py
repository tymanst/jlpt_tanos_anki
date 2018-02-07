import genanki
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

qa_temp = '''<style style="zoom: 1;">.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
</style><span style="font-family: Mincho; font-size: 72px; zoom: 1;">病院</span>
'''

af_temp = '''<span style="font-size: 22px; zoom: 1;">hospital</span><br style="zoom: 1;"><span style="font-family: Mincho; font-size: 32px; zoom: 1;">びょういん</span><br style="zoom: 1;">'''



def load_json():
    with open('jsondata.json') as data_file:
        data = json.load(data_file)

def main():
    deck = genanki.Deck(123123123123, 'foodeck1111')
    deck.add_note(genanki.Note(TEST_MODEL, [qa_temp , af_temp]))  # 2 cards
    genanki.Package(deck).write_to_file('output1.apkg')


if __name__ == '__main__':
    main()