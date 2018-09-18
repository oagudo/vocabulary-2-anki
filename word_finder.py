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


def contains_all_results(result):
    return result.meanings is not None and len(result.meanings) > 0 and result.examples is not None and \
           len(result.examples) > 0 and result.mp3_full_path is not None and result.image_full_path is not None


def combine_results(result, new_result):
    if len(result.meanings) == 0:
        result.meanings = new_result.meanings
    if len(result.examples) == 0:
        result.examples = new_result.examples
    if result.mp3_full_path is None:
        result.mp3_full_path = new_result.mp3_full_path
    if result.image_full_path is None:
        result.image_full_path = new_result.image_full_path
    return result


class Translator:
    def __init__(self, translators: List[WordTranslator]):
        self.translators = translators

    def find(self, word: str):

        result = TranslatorResult([], [], None, None)

        for t in self.translators:

            new_result = t.find(word)

            if contains_all_results(new_result):
                return new_result

            result = combine_results(result, new_result)

            if contains_all_results(result):
                return result

        return result


class TranslatorTest(unittest.TestCase):

    def setUp(self):
        self.dummy_result = TranslatorResult(['palabra'],
                                             ['Confio en tu palabra'],
                                             'mp3_full_path',
                                             'image_full_path')
        self.wt_1_mock = MagicMock()
        self.wt_2_mock = MagicMock()
        self.wt_3_mock = MagicMock()
        self.translator = Translator([self.wt_1_mock, self.wt_2_mock, self.wt_3_mock])

    def test_should_call_find_on_first_word_translator(self):
        self.wt_1_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result

    def test_should_call_find_until_getting_a_full_result(self):
        self.wt_1_mock.find.return_value = TranslatorResult([], [], None, None)
        self.wt_2_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result
        assert not self.wt_3_mock.find.called

    def test_should_collect_partial_results(self):
        self.wt_1_mock.find.return_value = TranslatorResult(["palabra"], [], None, None)
        self.wt_2_mock.find.return_value = TranslatorResult([], ["Confio en tu palabra"], "mp3_full_path",
                                                            "image_full_path")
        self.wt_3_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result
        assert not self.wt_3_mock.find.called


if __name__ == '__main__':
    unittest.main()
