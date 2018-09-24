import unittest
from unittest.mock import MagicMock

from vocabulary_builder.translator_result import TranslatorResult, Sense
from vocabulary_builder.translator import Translator


class TranslatorTest(unittest.TestCase):

    def setUp(self):
        sense = Sense(['palabra'], ['Confio en tu palabra'])
        self.dummy_result = TranslatorResult([sense], 'mp3_full_path')
        self.wt_1_mock = MagicMock()
        self.wt_2_mock = MagicMock()
        self.wt_3_mock = MagicMock()
        self.translator = Translator([self.wt_1_mock, self.wt_2_mock, self.wt_3_mock])

    def test_should_call_find_on_first_word_translator(self):
        self.wt_1_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result

    def test_should_call_find_until_getting_a_full_result(self):
        self.wt_1_mock.find.return_value = TranslatorResult.empty()
        self.wt_2_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result
        assert self.wt_2_mock.find.called
        assert not self.wt_3_mock.find.called

    def test_should_collect_partial_results(self):
        sense = Sense(['palabra'], ['Confio en tu palabra'])
        self.wt_1_mock.find.return_value = TranslatorResult([sense], None)
        self.wt_2_mock.find.return_value = TranslatorResult([], "mp3_full_path")
        self.wt_3_mock.find.return_value = self.dummy_result
        assert self.translator.find('word') == self.dummy_result
        assert not self.wt_3_mock.find.called
