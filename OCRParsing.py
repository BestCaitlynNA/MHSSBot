import re

import ScreenshotMetadata

def extract_entry(entries):
    entry_regex = r"(K[0-9]|K[:])"
    entry_list = []
    entry_list = re.split(entry_regex, entries)[1:]
    entry_list = entry_list[1::2]
    return entry_list

def extract_kingdom(entry):
    x_regex = r"( X[0-9]|X[:])"
    kingdom = re.split(x_regex, entry)[0]
    return kingdom
# Expected
# 163 X2309 Y:437 Monster Hunt Defeated Lv 2 Grim Reaper 04/29/18 06:51:16 %
def extract_x(entry):
    x_regex = r"(X[0-9]|X[:])"
    y_regex = r"( Y[0-9]|Y[:])"
    x_coordinate = re.split(x_regex, entry)[2]
    x_coordinate = re.split(y_regex, x_coordinate)[0]
    return validate_number(x_coordinate)

def extract_y(entry):
    y_regex = r"(Y[0-9]|Y[:])"
    monster_hunt_regex = r"( Monster Hunt )"
    y_coordinate = re.split(y_regex, entry)[2]
    y_coordinate = re.split(monster_hunt_regex, y_coordinate)[0]
    return validate_number(y_coordinate)

def extract_defeated(entry):
    defeated_regex = r"(Defeated)"
    defeated = re.split(defeated_regex, entry)[1].strip()
    return validate_defeated(defeated)

def extract_level(entry):
    level_regex = r"(Lv [1-5])"
    level = re.split(level_regex, entry)[1][-1:]
    return validate_number(level)

def extract_monster(entry):
    level_regex = r"(Lv [1-5] )"
    date_regex = r"( [0-1][0-9]/[0-3][0-9]/[0-9][0-9])"
    monster = re.split(level_regex, entry)[2]
    monster = re.split(date_regex, monster)[0]
    return validate_monster(monster)

def extract_date(entry):
    date_regex = r"([0-1][0-9]/[0-3][0-9]/[0-9][0-9])"
    date = re.split(date_regex, entry)[1]
    return date

def extract_time(entry):
    time_regex = r"([0-2][0-9]:[0-5][0-9]:[0-5][0-9])"
    time = re.split(time_regex, entry)[1]
    return time

def validate_monster(monster):
    if monster in Monsters.regular_monsters:
        return monster

def validate_number(number):
    if number.strip().isdigit():
        return number

def validate_defeated(defeated):
    if defeated.strip() is 'Defeated':
        return 'Defeated'

def get_valid_hunts(ocr_text_string):
    entries = extract_entry(ocr_text_string)
    valid_hunts = []
    for entry in entries:
        kingdom = extract_kingdom(entry)
        x = extract_x(entry)
        y = extract_y(entry)
        defeated = extract_defeated(entry)
        level = extract_level(entry)
        monster = extract_monster(entry)
        date = extract_date(entry)
        time = extract_time(entry)
        ssmd = ScreenshotMetadata.ScreenshotMetadata(kingdom, x, y, level, date, time, monster, defeated)
        if ssmd.Completed():
            valid_hunts.append(ssmd)
    return valid_hunts
