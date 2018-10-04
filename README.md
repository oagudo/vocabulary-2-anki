# Vocabulary builder for anki

## How to install the requirements

`$ pip install -r requirements.txt`

## How to build my own vocabulary deck for anki ?

1) Create a Oxford developer account at https://developer.oxforddictionaries.com/

2) Modify the configuration file `configuration/config.py` to include your api_key and app_id obtained in step 1.

3) Create a txt file containing all the words (one per line) that you would like to learn.

4) Place it at the root of the project (same level as `main.py`). You will need to provide its name inside the configuration file (it is called `vocabulary.txt` by default)

5) Change the language settings in the configuration file using IANA language two letters code (https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry). They will be used to translate you vocabulary from/to the selected languages.

6) run `python main.py` and wait for its completion

7) Import the anki deck file created as a result of the previous step (called `vocabulary.apkg` by default in the configuration)

8) Enjoy and learn :-)
