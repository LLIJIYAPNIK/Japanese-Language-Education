from sudachipy import Dictionary, SplitMode


tokenizer = Dictionary(dict="full").create()  # sudachidict_full

morphemes = tokenizer.tokenize("国会議事堂前駅")
print(morphemes[0].surface())  # '国会議事堂前駅'
print(morphemes[0].reading_form())  # 'コッカイギジドウマエエキ'
print(morphemes[0].part_of_speech())  # ['名詞', '固有名詞', '一般', '*', '*', '*']

morphemes = tokenizer.tokenize("国会議事堂前駅", SplitMode.A)
print([m.surface() for m in morphemes])  # ['国会', '議事', '堂', '前', '駅']


from tdmelodic.nn.lang.mecab.unidic import UniDic

u = UniDic(
    unidic_path=r"",
    mecabrc_path=r""
)
u.get_n_best("深層学習", "しんそうがくしゅう", 3)