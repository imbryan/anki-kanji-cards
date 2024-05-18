# Anki Kanji Cards
This is a script that generates Anki cards for a given list of kanji.

## Usage
Install dependencies:
```
pip install -r requirements.txt
```

Run script:
```
python kanji_cards.py <path_to_kanji_file> <path_to_output_file> [-d file_name]
```

> **path_to_kanji_file** is the relative path to a text file containing your kanji list. The script will ask you to specify how the kanji are separated. Personally, I used [nihongo-pro.com](https://www.nihongo-pro.com/kanji-pal/list/jlpt).
> **path_to_output_file** is the relative path (and name) of the file that will be created to contain your cards.
> **-d file_name** (optional) is the relative path to your current deck, exported (in Anki Notes format). This is only used in a comparison operation to avoid creating duplicate cards.

## Acknowledgements
This script makes use of the [jisho-api](https://github.com/pedroallenrevez/jisho-api) project, which scrapes [jisho.org](https://jisho.org) for data.