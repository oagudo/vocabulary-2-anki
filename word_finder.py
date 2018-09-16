import unittest
from typing import List


class FinderResult:
    def __init__(self, meanings: List[str]):
        self.meanings = meanings


class WordFinder:
    def __init__(self, from_lan: str, to_lan: str):
        self.to_lan = to_lan
        self.from_lan = from_lan

    def find(self, word: str) -> FinderResult:
        return FinderResult(['palabra'])


class WordFinderTest(unittest.TestCase):

    def setUp(self):
        self.finder = WordFinder('en', 'es')

    def test_should_find_word_meanings(self):
        result = self.finder.find('word')
        assert len(result.meanings) == 1
        assert result.meanings[0] == 'palabra'


if __name__ == '__main__':
    unittest.main()
