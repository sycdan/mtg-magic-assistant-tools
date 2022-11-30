"""
Import set data from MTGJSON format to Magic Assistant XML format.

Instructions:
- Download SET.json from https://mtgjson.com/downloads/all-sets/ and put in ./mtgjson
- Run script
- Close MA
- Copy output XML files to ./MagicAssistantWorkspace/magiccards/MagicDB
- Copy comment data from output files to ./MagicAssistantWorkspace/magiccards/MagicDB/tables/editions.txt
"""
import monkeypatches

import datetime as dt
import hashlib
import json
import os

from json2xml import json2xml

rarity_map = {
    'rare': "Rare",
    'uncommon': "Uncommon",
    'common': "Common",
    'mythic': "Mythic Rare",
}
input_dir = './mtgjson'
output_dir = f'./{input_dir}/output'
fieldnames = 'ID,NAME,SET,COLLNUM,COST,TYPE,POWER,TOUGHNESS,ORACLE,RARITY,ARTIST,RULINGS,TEXT,PROPERTIES,COMMENT,CUSTOM,SPECIAL,DATE'.split(',')


def escape_newlines(text):
    return text.replace('\r\n', '\n').replace('\n', '<br>')

def clean_set_name(name):
    return name.replace(' ', '_')

def clean_type(value):
    return value.replace('—', '-')


if __name__ != '__main__':
    exit()

try:
    os.mkdir(output_dir)
except:
    pass

for input_file in os.listdir(input_dir):
    if not input_file.endswith('.json'):
        continue

    input_path = f"{input_dir}/{input_file}"
    set_code = input_file.split('.')[0]
    print("Processing", input_path)

    mtgjson = json.load(open(input_path, encoding='utf-8'))
    setdata = mtgjson.pop('data')
    cards = setdata.pop('cards')
    print(json.dumps(setdata, indent=2, sort_keys=True))
    release_date = dt.datetime.strptime(setdata['releaseDate'], '%Y-%m-%d')
    release_date_display = release_date.strftime('%B %Y')
    set_name = setdata['name']
    cleaned_set_name = clean_set_name(set_name)
    output_file = f"{output_dir}/{cleaned_set_name}.xml"

    # Limited Edition Alpha|LEA|1E,A|August 1993|Core|Block|Format (probably leave blank)|Alpha Edition,Alpha
    edition_key = f"{set_name}|{set_code}||{release_date_display}|Expansion|||"

    output = dict(
        name=cleaned_set_name,
        key=cleaned_set_name,
        comment=edition_key,
        type='',
        list=[],
    )
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        sampled = False

        for row in cards:
            if not sampled:
                print("Sample card", row)
                sampled = True

            card_name = row['name']
            rarity = row['rarity']
            card_num = row['number']
            original_text = escape_newlines(row.get('originalText', ''))
            oracle_text = escape_newlines(row.get('text', ''))

            # Generate a hopefully unique id
            hash_key = f"{set_code}|{card_num}"
            card_id = -(int.from_bytes(hashlib.sha256(hash_key.encode('utf-8')).digest()[:4], 'little') // 10)

            card = {
                'id': f"{card_id}",  # This is the Gatherer ID, which is probably not available for sets MA doesn't know about
                'name': card_name,
                'cost': row.get('manaCost', ''),
                'type': clean_type(row.get('type', '')),
                'power': row.get('power', ''),
                'toughness': row.get('toughness', ''),
                'oracleText': oracle_text or original_text,
                'edition': set_name,
                'rarity': rarity_map[rarity],
                'artist': row.get('artist', ''),
                'num': card_num,
                'text': original_text or oracle_text,
            }
            output['list'].append({'mc': card})

        f.write(json2xml.Json2xml(output, wrapper='cards', item_wrap=False, attr_type=False).to_xml().decode('utf-8'))
