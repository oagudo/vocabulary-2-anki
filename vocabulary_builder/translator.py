from typing import List
from vocabulary_builder.translator_plugin import TranslatorPlugin
from vocabulary_builder.translator_result import TranslatorResult


def contains_all_results(result):
    return result.senses is not None and len(result.senses) > 0 and \
           result.mp3_full_path is not None


def combine_results(result, new_result):
    if len(result.senses) == 0:
        result.senses = new_result.senses
    if result.mp3_full_path is None:
        result.mp3_full_path = new_result.mp3_full_path
    return result


class Translator:
    def __init__(self, translators: List[TranslatorPlugin]):
        self.translators = translators

    def find(self, word: str):

        result = TranslatorResult([], None)

        for t in self.translators:
            new_result = t.find(word)
            if contains_all_results(new_result):
                return new_result

            result = combine_results(result, new_result)
            if contains_all_results(result):
                return result

        return result
