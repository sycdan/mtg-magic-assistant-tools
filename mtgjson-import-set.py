"""
Import set data from mtgjson format to Magic Assistant CSV format.

Instructions:
- Download SET.json from https://mtgjson.com/downloads/all-sets/ and put in ./mtgjson
- Run script
- Go to File -> Import -> Import New Set (Extend Database)
- Click New Set, enter the name and code from the MTGJSON data
- Open an output file and copy to clipboard
- Select Format: Magic Assistant CSV if not already selected

Output format:
ID,NAME,SET,COLLNUM,COST,TYPE,POWER,TOUGHNESS,ORACLE,RARITY,ARTIST,RULINGS,TEXT,PROPERTIES,COMMENT,CUSTOM,SPECIAL,DATE
,Consider,Wizards Play Network 2022,1,{U},Instant,,,Surveil 1. (Look at the top card of your library. You may put that card into your graveyard.)<br>Draw a card.,Rare,Zezhou Chen,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,Fateful Absence,Wizards Play Network 2022,2,{1}{W},Instant,,,"Destroy target creature or planeswalker. Its controller investigates. (Create a Clue token. It's an artifact with ""{2}, Sacrifice this artifact: Draw a card."")",Rare,Eric Deschamps,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,"Atsushi, the Blazing Sky",Wizards Play Network 2022,3,{2}{R}{R},Legendary Creature — Dragon Spirit,4,4,"Flying, trample<br>When Atsushi, the Blazing Sky dies, choose one —<br>• Exile the top two cards of your library. Until the end of your next turn, you may play those cards.<br>• Create three Treasure tokens.",Mythic Rare,Victor Adame Minguez,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,Swiftfoot Boots,Wizards Play Network 2022,4,{2},Artifact — Equipment,,,Equipped creature has hexproof and haste. (It can't be the target of spells or abilities your opponents control.)<br>Equip {1},Rare,Svetlin Velinov,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,Dismember,Wizards Play Network 2022,5,{1}{B/P}{B/P},Instant,,,({B/P} can be paid with either {B} or 2 life.)<br>Target creature gets -5/-5 until end of turn.,Rare,Alix Branwyn,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,Psychosis Crawler,Wizards Play Network 2022,6,{5},Artifact Creature — Phyrexian Horror,*,*,"Psychosis Crawler's power and toughness are each equal to the number of cards in your hand.<br>Whenever you draw a card, each opponent loses 1 life.",Rare,Stephan Martiniere,,,,,,,Sat Mar 05 23:59:59 UTC 2022
,Thought Vessel,Wizards Play Network 2022,7,{2},Artifact,,,You have no maximum hand size.<br>{T}: Add {C}.,Rare,Milivoj Ćeran,,,,,,,Sat Mar 05 23:59:59 UTC 2022
"""
import csv
import datetime as dt
import json
import os

rarity_map = {
    'rare': "Rare",
    'uncommon': "Uncommon",
    'common': "Common",
    'mythic': "Mythic Rare",
}
input_dir = './mtgjson'
fieldnames = 'ID,NAME,SET,COLLNUM,COST,TYPE,POWER,TOUGHNESS,ORACLE,RARITY,ARTIST,RULINGS,TEXT,PROPERTIES,COMMENT,CUSTOM,SPECIAL,DATE'.split(',')

if __name__ != '__main__':
    exit()

for input_file in os.listdir(input_dir):
    if not input_file.endswith('.json'):
        continue

    input_path = f"{input_dir}/{input_file}"
    set_code = input_file.split('.')[0]
    output_file = f"mtgassistant-set-{set_code}.csv"
    print("Processing", input_path)

    mtgjson = json.load(open(input_path, encoding='utf-8'))
    setdata = mtgjson.pop('data')
    cards = setdata.pop('cards')
    print(json.dumps(setdata, indent=2, sort_keys=True))
    release_date = dt.datetime.strptime(setdata['releaseDate'], '%Y-%m-%d')
    set_name = setdata['name']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        sampled = False

        for row in cards:
            if not sampled:
                print("Sample card", row)
                sampled = True

            card_name = row['name']
            rarity = row['rarity']
            card_num = row['number']

            # Probably just a foil version of another card if the file
            # and MA will just overwrite the non-star version.
            if card_num.endswith('★'):
                continue

            writer.writerow({
                'ID': '',  # This is the Gatherer ID, which is probably not available for sets MA doesn't know about
                'NAME': card_name,
                'SET': set_name,
                'COST': row.get('manaCost', ''),
                'RARITY': rarity_map[rarity],
                'TYPE': row.get('type', ''),
                'POWER': row.get('power', ''),
                'TOUGHNESS': row.get('toughness', ''),
                'ORACLE': row.get('text', '').replace('\r\n', '\n').replace('\n', '<br>'),
                'TEXT': row.get('originalText', '').replace('\r\n', '\n').replace('\n', '<br>'),
                'ARTIST': row.get('artist', ''),
                'COLLNUM': card_num,
                'DATE': release_date.strftime('%a %b %d 23:59:59 UTC %Y'),
            })
