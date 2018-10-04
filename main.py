import os
import genanki
import random
from utils.format import *
from vocabulary_builder.translator_result import TranslatorResult
from vocabulary_builder.plugins.oxford_translator import OxfordTranslator
from vocabulary_builder.translator import Translator
from configuration.config import GLOBAL_CFG

model_id = random.randrange(1 << 30, 1 << 31)
vocabulary_model = genanki.Model(
    model_id,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])

deck_id = random.randrange(1 << 30, 1 << 31)
vocabulary_deck = genanki.Deck(deck_id, GLOBAL_CFG['anki']['deck_name'])


def get_words_to_find():
    words = []
    with open(GLOBAL_CFG['vocabulary_file_name'], "r") as ins:
        for line in ins:
            line = line.rstrip("\n")
            words.append(line)
    return words


oxford_translator = OxfordTranslator(GLOBAL_CFG['language']['from'], GLOBAL_CFG['language']['to'])
translator = Translator([oxford_translator])

mp3_files = []
not_founds = []
words = get_words_to_find()
for word in words:
    print("Searching for word %s" % word)

    result = translator.find(word)

    if result.mp3_full_path:
        mp3_files.append(result.mp3_full_path)

    if result == TranslatorResult.empty():
        not_founds.append(word)
    else:
        new_note = genanki.Note(
            model=vocabulary_model,
            fields=["<h1>" + word + "</h1>", format_sound(result.mp3_full_path) + '\n\n' + format_senses(result)])
        vocabulary_deck.add_note(new_note)

genanki.Package(vocabulary_deck, media_files=mp3_files).write_to_file(GLOBAL_CFG['anki']['deck_file_name'])

if len(not_founds) > 0:
    print("words not found :")
    for nf in not_founds:
        print(nf)

for sound_file in mp3_files:
    os.remove(sound_file)
