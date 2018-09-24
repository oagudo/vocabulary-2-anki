from typing import List, Optional


class Sense:
    def __init__(self, meanings: str, examples: List[str]):

        if not isinstance(meanings, list):
            raise TypeError('meaning should be a list')

        if not isinstance(examples, list):
            raise TypeError('examples should be a list')

        self.meanings = meanings
        self.examples = examples

    def __str__(self):
        return str(self.meanings) + " " + str(self.examples)

    def __eq__(self, other):
        return (self.meanings == other.meanings) and (self.examples == other.examples)


class TranslatorResult:
    def __init__(self, senses: List[Sense], mp3_full_path: Optional[str]):

        if not isinstance(senses, list):
            raise TypeError('senses should be a list')

        if not isinstance(mp3_full_path, str) and not isinstance(mp3_full_path, type(None)):
            raise TypeError('mp3_full_path should be a Optional[str]')

        self.senses = senses
        self.mp3_full_path = mp3_full_path

    @staticmethod
    def empty():
        return TranslatorResult([], None)

    def __str__(self):
        return str(self.senses) + " " + str(self.mp3_full_path)

    def __eq__(self, other):
        return (self.senses == other.senses) and (
                self.mp3_full_path == other.mp3_full_path)
