# Vocabulary builder for anki

## Requirements

Python3. Dependencies can be installed with:

`$ pip3 install -r requirements.txt`

## How to build your own vocabulary deck for anki ?

1) Create an [Oxford developer account](https://developer.oxforddictionaries.com/)

2) Modify the configuration file `configuration/config.py` to include your `api_key` and `app_id` values obtained in step 1.

3) Fill the `vocabulary.txt` file with the words that you would like to learn (one per line).

4) Change the language settings in the configuration file using [IANA two letters codes](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry). They will be used to translate your vocabulary list from/to the selected languages.

5) run `python3 main.py` and wait for its completion

6) Import the anki deck file created as a result of the previous step (it is called `vocabulary.apkg` by default, but you can change its name in the configuration)

7) Enjoy and learn :-)