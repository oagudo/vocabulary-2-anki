import requests
import urllib
from utils.optional_dict import OptDict
from vocabulary_builder.translator_result import TranslatorResult, Sense
from vocabulary_builder.translator_plugin import TranslatorPlugin
from configuration.config import OXFORD_PLUGIN_CFG


class OxfordTranslator(TranslatorPlugin):
    def __init__(self, from_lan: str, to_lan: str):
        self.base_url = "https://od-api.oxforddictionaries.com/api/v1"
        self.api_key = OXFORD_PLUGIN_CFG['api_key']
        self.app_id = OXFORD_PLUGIN_CFG['app_id']
        super(OxfordTranslator, self).__init__('Oxford translator', from_lan, to_lan)

    def find(self, word: str) -> TranslatorResult:

        t_result = TranslatorResult.empty()

        # Translations
        url = self.base_url + '/entries/' + self.from_lan + '/' + word + '/translations=' + self.to_lan
        r = requests.get(url, headers={'app_id': self.app_id, 'app_key': self.api_key})

        if r.status_code == 200:
            response = OptDict.from_dict(r.json())
            for result in response.get("results", []):
                for le in result.get("lexicalEntries", []):
                    for entry in le.get("entries", []):
                        for sense in entry.get("senses", []):

                            new_sense = Sense([], [])

                            translations = sense.get("translations", [])
                            notes = sense.get("notes", [])
                            definitions = sense.get("definitions", [])

                            for sub in sense.get("subsenses", []):
                                translations = translations + sub.get("translations", [])
                                notes = notes + sub.get("notes", [])
                                definitions = definitions + sub.get("definitions", [])

                            for translation in translations:
                                translation_text = translation["text"]
                                new_sense.meanings.append(translation_text)

                            for d in definitions:
                                new_sense.meanings.append(d)

                            for note in notes:
                                note_txt = note.get('text', None)
                                if note_txt:
                                    new_sense.meanings.append("(" + note_txt + ")")

                            examples = sense.get("examples", [])
                            for sub in sense.get("subsenses", []):
                                examples = examples + sub.get("examples", [])

                            for ex in examples:
                                text_original_lan = ex.get("text", "")
                                text_translated_lan = ex.get("translations", [{"text": ""}])[0]["text"]
                                new_sense.examples.append(text_original_lan + " -> " + text_translated_lan)

                            t_result.senses.append(new_sense)

        # Pronunciation and meaning
        url = self.base_url + '/entries/' + self.from_lan + '/' + word.lower()
        r = requests.get(url, headers={'app_id': self.app_id, 'app_key': self.api_key})

        if r.status_code == 200:

            response = OptDict.from_dict(r.json())
            for result in response.get("results", []):
                for le in result.get("lexicalEntries", []):
                    for p in le.get("pronunciations", []):
                        if "british" in p.get("dialects", [""])[0].lower():
                            if "audioFile" in p:
                                location = p["audioFile"]
                                audio_name = location.split("/")[-1]
                                urllib.request.urlretrieve(location, audio_name)
                                t_result.mp3_full_path = audio_name

        return t_result
