import unittest

from vocabulary_builder.translator_result import TranslatorResult, Sense
from vocabulary_builder.translator_plugin import TranslatorPlugin


class DummyTranslatorPlugin(TranslatorPlugin):
    def __init__(self, from_lan: str, to_lan: str):
        super(DummyTranslatorPlugin, self).__init__('dummy word_translator', from_lan, to_lan)

    def find(self, word: str) -> TranslatorResult:
        return TranslatorResult([Sense(['palabra'],
                                       ['Confio en tu palabra', 'No tengo palabras'])],
                                'mp3_full_path')


class WordTranslatorTest(unittest.TestCase):

    def setUp(self):
        self.word_translator = DummyTranslatorPlugin('en', 'es')

    def test_should_have_a_name(self):
        assert self.word_translator.name == 'dummy word_translator'

    def test_should_find_word_meanings(self):
        result = self.word_translator.find('word')
        assert len(result.senses) == 1
        assert result.senses[0].meanings[0] == 'palabra'

    def test_should_find_word_examples(self):
        result = self.word_translator.find('word')
        assert len(result.senses) == 1
        assert result.senses[0].examples[0] == 'Confio en tu palabra'
        assert result.senses[0].examples[1] == 'No tengo palabras'

    def test_should_find_pronunciation_mp3_file(self):
        result = self.word_translator.find('word')
        assert isinstance(result.mp3_full_path, str)
