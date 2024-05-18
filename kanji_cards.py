import argparse, csv, sys, time
# import requests
# from bs4 import BeautifulSoup
from jisho_api.kanji import Kanji

parser = argparse.ArgumentParser()
parser.add_argument('kanji_file', type=str, help='.txt file with the Kanji to create cards for')
parser.add_argument('output_file', type=str, help='name the file that the new cards will be written to')
parser.add_argument('-d', type=str, help='deck _notes.txt file exported from Anki (to check for duplicate Kanji)')
args = parser.parse_args()
kanji_file_loc = args.kanji_file
output_file_loc = args.output_file
current_deck_loc = args.d
kanji = []
deck = []
start_time = time.time()

try:
    with open(kanji_file_loc, 'r', encoding='utf-8') as kanji_file:
        field_headers = input('Enter your deck\'s card fields in order, separated only by commas (leave blank for the Anki default "Front,Back"): ') or 'Front,Back'
        field_headers = field_headers.lower().split(',')
        data_map = {
            'front': ['front',],
            'back': ['back',],
        }
        if 'front' not in field_headers:
            data_map['front'] = [ input('Specify the name of which header represents the term: ').lower(), ]
        if 'back' not in field_headers:
            data_map['back'] = [ input('Specify the name of which header represents the definition: ').lower(), ]
        delim = input(f'Enter the Kanji delimiter for "{kanji_file_loc.split('/')[-1]}" (leave blank for space): ') or ' '
        kanji = kanji_file.read().split(delim)
        
        # Optionally read current deck
        if current_deck_loc:
            try:
                with open(current_deck_loc, 'r', encoding='utf-8') as deck_file:
                    for line in deck_file:
                        if line[0] != '#':  # ignore comments
                            deck.append(line.split('\t')[0])

                    kanji_len_before = len(kanji)
                    kanji = [item for item in kanji if item not in deck]
                    print(f'Skipping {kanji_len_before - len(kanji)} duplicate Kanji...')
            except (FileNotFoundError, IOError) as e:
                print(f'Error: {e}')
                sys.exit()
                
        print(f'Making {len(kanji)} cards...')

        if output_file_loc.endswith(".csv") == False:
            output_file_loc = f'{output_file_loc}.csv'
        with open(output_file_loc, mode='w', newline='', encoding='utf-8') as output_file:
            write = csv.DictWriter(output_file, fieldnames=field_headers)
            # write.writeheader()  # Not needed in Anki
            for index, kanji_str in enumerate(kanji):
                r = Kanji.request(kanji_str)
                # NOTE making my own request here because:
                # jisho_api.kanji.Kanji.request.data.meta.education.jlpt is always returned as None 
                # r2 = requests.get(f'https://jisho.org/search/{kanji_str}%23kanji').content
                # soup = BeautifulSoup(r2, "html.parser")
                # jlpt = soup.find_all("div", {"class": "kanji_stats"})[0].find_all("div", {"class": "jlpt"})[0].find_all("strong")[0].text
                # NOTE 2 ultimately decided against the second request, since users can tag cards on the Anki import interface, it's not worth doubling the # of requests
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # print(f'{0}:{kanji[0]},{r.data.radical.basis},{r.data.main_meanings},{r.data.main_readings},{jlpt}')
                row_data = {}
                if field_headers == ['front','back']:
                    row_data['front'] = kanji_str
                    row_data['back'] = ', '.join(r.data.main_meanings)
                    if r.data.radical.basis:
                        row_data['back'] = f'{row_data["back"]}<br />{r.data.radical.basis}'
                    if r.data.main_readings:
                        joined_readings = '、'.join((r.data.main_readings.on or []) + (r.data.main_readings.kun or []))
                        row_data['back'] = f'{row_data["back"]}<br />{joined_readings}'
                else:
                    # TODO Currently, for users with non-standard headings that don't specify 'radical' and 'reading' headings, their output will not have those data
                    for header in field_headers:
                        if header in data_map['front']:
                            row_data[header] = kanji_str
                        elif header in data_map['back']:
                            row_data[header] = ', '.join(r.data.main_meanings)
                        elif header == 'radical':
                            row_data[header] = r.data.radical.basis
                        elif header == 'reading':
                            row_data[header] = '、'.join((r.data.main_readings.on or []) + (r.data.main_readings.kun or []))
                # row_data['tags'] = jlpt
                write.writerow(row_data)

                # Console feedback
                print(f'{index+1}...')
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f'Done. Took {time_elapsed:.2f} seconds.')
except (FileNotFoundError, IOError) as e:
    print(f'Error: {e}')

