from sudachipy import Dictionary, SplitMode


tokenizer = Dictionary(dict="full").create()  # sudachidict_full

morphemes = tokenizer.tokenize("国会議事堂前駅")
print(morphemes[0].surface())  # '国会議事堂前駅'
print(morphemes[0].reading_form())  # 'コッカイギジドウマエエキ'
print(morphemes[0].part_of_speech())  # ['名詞', '固有名詞', '一般', '*', '*', '*']
print([m.surface() for m in morphemes])  # ['国会', '議事', '堂', '前', '駅']

tokenizer = Dictionary(dict="full").create()
morphemes = tokenizer.tokenize("国会議事堂前駅", SplitMode.C)
print([m.surface() for m in morphemes])  # ['国会', '議事', '堂', '前', '駅']


from tdmelodic.nn.lang.mecab.unidic import UniDic

u = UniDic()
for m in morphemes:
    print(m.surface())
    print(u.get_n_best(m.surface(), m.reading_form())[0][0][0])
print(u.get_n_best(morphemes[0].surface(), morphemes[0].reading_form())[0][0][0])