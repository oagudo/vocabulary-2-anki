import unittest
from unittest.mock import MagicMock
from typing import List, Optional
import abc


class TranslatorResult:
    def __init__(self, meanings: List[str], examples: List[str], mp3_full_path: Optional[str],
                 image_full_path: Optional[str]):
        self.meanings = meanings
        self.examples = examples
        self.mp3_full_path = mp3_full_path
        self.image_full_path = image_full_path

    def __eq__(self, other):
        return (self.meanings == other.meanings) and (self.examples == other.examples) and (
                    self.mp3_full_path == other.mp3_full_path) and (self.image_full_path == other.image_full_path)


class WordTranslator(metaclass=abc.ABCMeta):

    def __init__(self, name: str, from_lan: str, to_lan: str):
        self.name = name
        self.to_lan = to_lan
        self.from_lan = from_lan

    def name(self):
        return self.name

    @abc.abstractmethod
    def find(self, word: str) -> TranslatorResult:
        pass


class DummyWordTranslator(WordTranslator):
    def __init__(self, from_lan: str, to_lan: str):
        super(DummyWordTranslator, self).__init__('dummy word_translator', from_lan, to_lan)

    def find(self, word: str) -> TranslatorResult:
        return TranslatorResult(['palabra'],
                                ['Confio en tu palabra', 'No tengo palabras'],
                                'mp3_full_path',
                                'image_full_path')


class WordTranslatorTest(unittest.TestCase):

    def setUp(self):
        self.word_translator = DummyWordTranslator('en', 'es')

    def test_should_have_a_name(self):
        assert self.word_translator.name == 'dummy word_translator'

    def test_should_find_word_meanings(self):
        result = self.word_translator.find('word')
        assert len(result.meanings) == 1
        assert result.meanings[0] == 'palabra'

    def test_should_find_word_examples(self):
        result = self.word_translator.find('word')
        assert len(result.examples) == 2
        assert result.examples[0] == 'Confio en tu palabra'
        assert result.examples[1] == 'No tengo palabras'

    def test_should_find_pronunciation_mp3_file(self):
        result = self.word_translator.find('word')
        assert isinstance(result.mp3_full_path, str)

    def test_should_find_an_image_of_the_world(self):
        result = self.word_translator.find('word')
        assert isinstance(result.image_full_path, str)


class Translator:
    def __init__(self, translators: List[WordTranslator]):
        self.translators = translators

    def find(self, word: str):
        return self.translators[0].find(word)


class TranslatorTest(unittest.TestCase):

    def setUp(self):
        self.dummy_result = TranslatorResult(['palabra'],
                                             ['Confio en tu palabra', 'No tengo palabras'],
                                             'mp3_full_path',
                                             'image_full_path')
        word_translator_mock = MagicMock()
        word_translator_mock.find.return_value = self.dummy_result
        self.translator = Translator([word_translator_mock])

    def test_call_find_on_word_translators(self):
        assert self.translator.find('word') == self.dummy_result


if __name__ == '__main__':
    unittest.main()
