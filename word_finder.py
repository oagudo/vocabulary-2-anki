import unittest
from typing import List, Optional
import abc


class FinderResult:
    def __init__(self, meanings: List[str], examples: List[str], mp3_full_path: Optional[str],
                 image_full_path: Optional[str]):
        self.meanings = meanings
        self.examples = examples
        self.mp3_full_path = mp3_full_path
        self.image_full_path = image_full_path


class WordFinder(metaclass=abc.ABCMeta):

    def __init__(self, name: str, from_lan: str, to_lan: str):
        self.name = name
        self.to_lan = to_lan
        self.from_lan = from_lan

    def name(self):
        return self.name

    @abc.abstractmethod
    def find(self, word: str) -> FinderResult:
        pass


class DummyWordFinder(WordFinder):
    def __init__(self, from_lan: str, to_lan: str):
        super(DummyWordFinder, self).__init__('dummy finder', from_lan, to_lan)

    def find(self, word: str) -> FinderResult:
        return FinderResult(['palabra'],
                            ['Confio en tu palabra', 'No tengo palabras'],
                            'mp3_full_path',
                            'image_full_path')


class WordFinderTest(unittest.TestCase):

    def setUp(self):
        self.finder = DummyWordFinder('en', 'es')

    def test_should_have_a_name(self):
        assert self.finder.name == 'dummy finder'

    def test_should_find_word_meanings(self):
        result = self.finder.find('word')
        assert len(result.meanings) == 1
        assert result.meanings[0] == 'palabra'

    def test_should_find_word_examples(self):
        result = self.finder.find('word')
        assert len(result.examples) == 2
        assert result.examples[0] == 'Confio en tu palabra'
        assert result.examples[1] == 'No tengo palabras'

    def test_should_find_pronunciation_mp3_file(self):
        result = self.finder.find('word')
        assert isinstance(result.mp3_full_path, str)

    def test_should_find_an_image_of_the_world(self):
        result = self.finder.find('word')
        assert isinstance(result.image_full_path, str)


if __name__ == '__main__':
    unittest.main()
