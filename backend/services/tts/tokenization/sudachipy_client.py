from sudachipy import Dictionary, SplitMode
from sudachipy.sudachipy import MorphemeList, Morpheme


class SudachiPyClient:
    def __init__(self, dictionary: Dictionary) -> None:
        self.dictionary = dictionary
        self.tokenizer = self.dictionary.create()

    def _tokenize(self, text, mode) -> list:
        if not text or not text.strip():
            return []
        morphemes = self.tokenizer.tokenize(text, mode)
        return [m.surface() for m in morphemes]

    def tokenize_by_every_part(self, text) -> list:
        return self._tokenize(text, SplitMode.A)

    def tokenize_by_words(self, text) -> list:
        return self._tokenize(text, SplitMode.B)

    def tokenize_by_mean(self, text) -> list:
        return self._tokenize(text, SplitMode.C)

    @staticmethod
    def get_reading(morpheme: Morpheme) -> str:
        if morpheme:
            return morpheme.reading_form()
        else:
            return ""

    @staticmethod
    def get_readings(morphemes: MorphemeList) -> list:
        return [morpheme.reading_form() for morpheme in morphemes]
