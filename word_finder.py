import unittest
from typing import List
import abc


class FinderResult:
    def __init__(self, meanings: List[str], examples: List[str]):
        self.meanings = meanings
        self.examples = examples


class WordFinder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self, word: str) -> FinderResult:
        pass


class DummyWordFinder(WordFinder):
    def __init__(self, from_lan: str, to_lan: str):
        self.to_lan = to_lan
        self.from_lan = from_lan

    def find(self, word: str) -> FinderResult:
        return FinderResult(['palabra'],
                            ['Confio en tu palabra', 'No tengo palabras'])


class WordFinderTest(unittest.TestCase):

    def setUp(self):
        self.finder = DummyWordFinder('en', 'es')

    def test_should_find_word_meanings(self):
        result = self.finder.find('word')
        assert len(result.meanings) == 1
        assert result.meanings[0] == 'palabra'

    def test_should_find_word_examples(self):
        result = self.finder.find('word')
        assert len(result.examples) == 2
        assert result.examples[0] == 'Confio en tu palabra'
        assert result.examples[1] == 'No tengo palabras'


if __name__ == '__main__':
    unittest.main()
