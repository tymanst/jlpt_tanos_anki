import json

kanjies = {}

for i in range(1, 6):
    with open('json/KanjiList.N' + str(i) + '.json', 'r') as outfile:
        print('json/KanjiList.N' + str(i) + '.json')
        list = json.load(outfile)
        values = [el["kanji"] for el in list]
        kanjies[i] = values

res = []

for i in kanjies:
    for el in kanjies[i]:
        for j in range(i+1, len(kanjies)+1):
            print(el, i, j)
            if el in kanjies[j]:
                res.append((el, i, j))

