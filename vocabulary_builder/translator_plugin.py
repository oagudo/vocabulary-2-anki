import abc

from vocabulary_builder.translator_result import TranslatorResult


class TranslatorPlugin(metaclass=abc.ABCMeta):

    def __init__(self, name: str, from_lan: str, to_lan: str):
        self.name = name
        self.to_lan = to_lan
        self.from_lan = from_lan

    def name(self):
        return self.name

    @abc.abstractmethod
    def find(self, word: str) -> TranslatorResult:
        pass
