"""
Convert Dragon Shield MTG Card Manager all-folders.csv to Magic Assistant CSV.

"sep=," line must be removed from input first.

One output file will be created for each folder.

Output example:
ID,NAME,COST,TYPE,POWER,TOUGHNESS,ORACLE,SET,RARITY,DBPRICE,LANG,RATING,ARTIST,COLLNUM,RULINGS,TEXT,ENID,PROPERTIES,COUNT,PRICE,COMMENT,LOCATION,CUSTOM,OWNERSHIP,SPECIAL,DATE
106384,Reya Dawnbringer,{6}{W}{W}{W},Legendary Creature - Angel,4,6,,Tenth Edition,,0.0,,0.0,,,,"Flying<br>At the beginning of your upkeep, you may return target creature card from your graveyard to the battlefield.",0,,4,0.0,,,,false,,Tue Nov 29 21:32:00 EST 2022
191313,Platinum Angel,{7},Artifact Creature - Angel,4,4,,Magic 2010,,0.0,,0.0,,,,Flying<br>You can't lose the game and your opponents can't win the game.,0,,3,0.0,,,,false,"foil,c=good",Tue Nov 29 21:32:00 EST 2022
196998,Reya Dawnbringer,{6}{W}{W}{W},Legendary Creature - Angel,4,6,,Duel Decks: Divine vs. Demonic,,0.0,,0.0,,,,"Flying<br>At the beginning of your upkeep, you may return target creature card from your graveyard to the battlefield.",0,,3,0.0,,,,false,c=heavily_played,Tue Nov 29 21:32:00 EST 2022
196998,Reya Dawnbringer,{6}{W}{W}{W},Legendary Creature - Angel,4,6,,Duel Decks: Divine vs. Demonic,,0.0,,0.0,,,,"Flying<br>At the beginning of your upkeep, you may return target creature card from your graveyard to the battlefield.",0,,1,0.0,,,,false,"c=heavily_played,fortrade",Tue Nov 29 21:32:00 EST 2022

"""
import os
import re
import csv
from datetime import datetime
from decimal import Decimal
from sys import argv

input_file = 'all-folders.csv'
output_dir = './output'
output_file_base = '{}.csv'
writers = {}
fieldnames = 'NAME,SET,COLLNUM,LANG,COUNT,PRICE,COMMENT,LOCATION,CUSTOM,OWNERSHIP,SPECIAL,DATE'.split(',')

set_map = {
    # 'PHOP': '__SKIP__',
    'AFC': 'Adventures in the Forgotten Realms Commander',
    'C20': 'Ikoria Commander',
    'CMD': 'Magic: The Gathering-Commander',
    'MIC': 'Innistrad: Midnight Hunt Commander',
    'MM3': 'Modern Masters 2017 Edition',
    'NCC': 'Streets of New Capenna Commander',
    'PPRE': 'Promo set for Gatherer',
    'PVAN': 'Vanguard',
    'OPC2': 'Planechase 2012 Edition',
    'TBRO': '__SKIP__',
    'TSB': 'Time Spiral "Timeshifted"',
}

name_map = {
    'Chaotic Aether': 'Chaotic Æther',
    'Knight of Dawn': 'Knight Of Dawn (Knight of Dawn)',
}

lang_map = {
}

if __name__ != '__main__':
    exit()

try:
    os.mkdir(output_dir)
except:
    pass


# FUNCTIONS

def get_writer(folder_name):
    if folder_name not in writers:
        f = open(f"{output_dir}/{output_file_base}".replace('{}', folder_name), 'w', newline='', encoding='utf-8')
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writers[folder_name] = [f, writer]
    return writers[folder_name][1]

def close_output_files():
    for f in writers:
        writers[f][0].close()

def render_card_number(card_number, card_name):
    if '//' in card_name:
        return True
    if re.match('[a-zA-Z]', card_number):
        return True
    return False


# MAIN

reader = csv.DictReader(open(argv[1] if len(argv) > 1 else input_file, encoding='utf-8'))

for row in reader:
    writer = get_writer(row['Folder Name'])
    comments = []
    tags = ['condition:' + row['Condition']]
    card_name = name_map.get(row['Card Name'], row['Card Name'])

    set_name = row['Set Name']
    set_code = row['Set Code']
    mapped_set_name = set_map.get(set_code, set_name)
    if mapped_set_name == '__SKIP__':
        continue

    if set_code.startswith('P') and set_name.endswith(' Promos'):
        mapped_set_name = set_name[0:-7]
        tags.append('promo')

    card_number = row['Card Number']
    remap_key = set_code + '|' + card_number
    if remap_key in set_map:
        comments.append('Original number: ' + card_number)
        mapped_set_name = set_map[remap_key]

    if set_name != mapped_set_name:
        comments.append("Orignial set name: " + set_name)

    printing = row['Printing']
    language = row['Language']
    
    date_bought = datetime.strptime(row['Date Bought'], '%Y-%m-%d')
    price_bought = Decimal(row['Price Bought'])

    if printing == 'Foil':
        tags.append('foil')

    writer.writerow({
        'NAME': card_name,
        'SET': mapped_set_name,
        'COLLNUM': card_number if render_card_number(card_number, card_name) else '',
        'LANG': lang_map.get(language, language),
        'COUNT': row['Quantity'],
        'PRICE': "{:.2f}".format(price_bought),
        'DATE': date_bought.strftime('%a %b %d 23:59:59 UTC %Y'),
        'COMMENT': '; '.join(comments),
        'OWNERSHIP': 'true',  # vs physical
        'SPECIAL': ','.join(tags),
    })

close_output_files()