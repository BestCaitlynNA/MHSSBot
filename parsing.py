#!/usr/bin/env python3
#import ScreenshotProcessing
import re

import ScreenshotMetadata
import Monsters

screenshot1 = ['K2163', 'X1299', 'Y:447', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Grim', 'Reaper', '04/29/18', '13:43:09', '‘', '%', 'K2163', 'X2309','Y:437', 'Monster', 'Hunt','Defeated', 'Lv', '2', 'Grim', 'Reaper', '04/29/18', '06:51:16', '%', 'K2163', 'X2299', 'Y:415', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Mega', 'Maggot', '04/28/18', '22:00:38', '%', 'K2163', 'X2279', 'Y:423', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Mega', 'Maggot', '04/28/18', '14:34:52', '%', 'K2163', 'X:299', 'Y:425', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Blackwing', '04/28/18', '12:12:11', 'S', '4,?']
screenshot2 = ['K2163', 'X2288', 'Y2434', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Queen', 'Bee', '05/01/18', '16:27:38', '%', 'K2163', 'X2303', 'Y2431', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Saberfang', '05/01/18', '16:25:28', '%', 'K2163', 'X2326', 'Y:426', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Queen', 'Bee', '05/01/18', '05:43:16', '%', 'K2163', 'X2291', 'Y:417', 'Monster', 'Hunt', 'Defeated', 'Lv', '2', 'Saberfang', '05/01/18', '05:41:53', '%', 'K2163', 'X2301', 'Y:423', 'Monster', 'Hunt', 'Defeated', 'LV', '2', 'Queen', 'Bee', '04/30/18', '18:15:10']


# def Init_MHSSMD():
#     return ScreenshotMetadata()

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
    x_coordinate = re.split(y_regex, x_coordinate)[0][:-1]
    return x_coordinate

def extract_y(entry):
    y_regex = r"(Y[0-9]|Y[:])"
    monster_hunt_regex = r"( Monster Hunt )"
    y_coordinate = re.split(y_regex, entry)[2]
    y_coordinate = re.split(monster_hunt_regex, y_coordinate)[0]
    return y_coordinate

def extract_defeated(entry):
    defeated_regex = r"(Defeated)"
    defeated = re.split(defeated_regex, entry)[1]
    return defeated

def extract_level(entry):
    level_regex = r"(Lv [1-5])"
    level = re.split(level_regex, entry)[1][-1:]
    print('length: ',len(level))
    return level

def extract_monster(entry):
    level_regex = r"(Lv [1-5] )"
    date_regex = r"( [0-1][0-9]/[0-3][0-9]/[0-9][0-9])"
    monster = re.split(level_regex, entry)[2]
    monster = re.split(date_regex, monster)[0]
    return monster

def extract_date(entry):
    date_regex = r"([0-1][0-9]/[0-3][0-9]/[0-9][0-9])"
    date = re.split(date_regex, entry)[1]
    return date

def extract_time(entry):
    time_regex = r"([0-2][0-9]:[0-5][0-9]:[0-5][0-9])"
    time = re.split(time_regex, entry)[1]
    return time

if __name__ == '__main__':
    ss1_string = " ".join(screenshot1)
    matches = extract_entry(ss1_string)
    print(ss1_string)
    for match in matches:
        print(match)
    print(extract_kingdom(matches[0]))
    print(extract_x(matches[0]))
    print(extract_y(matches[0]))
    print(extract_defeated(matches[0]))
    print(extract_level(matches[0]))
    print(extract_monster(matches[0]))
    print(extract_date(matches[0]))
    print(extract_time(matches[0]))
    #print(ss1_string)
    '''
    #Regex K: or K# to find start of entry -> split entry up this way
    entry_regex = r"(K[0-9]|K[:])"
    x_regex = r"(X[0-9]|X[:])"
    y_regex = r"(Y[0-9]|Y[:])"
    level_regex = r"( [1-5] )"
    date_regex = r"([0-1][0-9]/[0-3][0-9]/[0-9][0-9])"
    time_regex = r"([0-2][0-9]:[0-5][0-9]:[0-5][0-9])"
    kingdom_matches = re.split(entry_regex, ss1_string)[0::2]
    monster_screenshot_metadata_list = [ScreenshotMetadata.ScreenshotMetadata() for _ in range(len(kingdom_matches))]
    print(len(monster_screenshot_metadata_list))
    for kingdom_match in kingdom_matches:
        #do the same to find x and y coordinates
        x_matches = re.split(x_regex, kingdom_match)[2::3]
        for i, x_match in enumerate(x_matches):
            y_matches = re.split(y_regex, x_match)
            x_coordinates = y_matches[0::3]
            for j, x_coordinate in enumerate(x_coordinates):
                x_coordinate = x_coordinate[:-1]
                monster_screenshot_metadata_list[j].x = x_coordinate
            y_matches = y_matches[2::3]
            for j, y_match in enumerate(y_matches):
                level_matches = re.split(level_regex, y_match)
                y_coordinates = level_matches[0::3]
                for k, y_coordinate in enumerate(y_coordinates):
                    y_coordinate = y_coordinate.split()[0]
                    monster_screenshot_metadata_list[k].y = y_coordinate
                levels = level_matches[1::3]
                for l, level in enumerate(levels):
                    monster_screenshot_metadata_list[l].level = level[1]
                level_matches = level_matches[2::3]
                for k, level_match in enumerate(level_matches):
                    date_matches = re.split(date_regex, level_match)
                    monster_matches = date_matches[0::3]
                    for l, monster_match in enumerate(monster_matches):
                        monster_match = monster_match[:-1]
                        if monster_match in Monsters.regular_monsters:
                            monster_screenshot_metadata_list[l].monster_name = monster_match
                    time_strings = date_matches[2::3]
                    date_matches = date_matches[1::3]
                    for l, date_match in enumerate(date_matches):
                        monster_screenshot_metadata_list[l].date = date_match
                    for l, time_string in enumerate(time_strings):
                        time_matches = re.split(time_regex, time_string)[1::3]
                        for m, time_match in enumerate(time_matches):
                            monster_screenshot_metadata_list[m].time = time_match
    for monster_screenshot_metadata in monster_screenshot_metadata_list:
        print(monster_screenshot_metadata)
    #    if (not monster_screenshot_metadata.Completed()):
    #        monster_screenshot_metadata_list.remove(monster_screenshot_metadata)
    #for monster_screenshot_metadata in monster_screenshot_metadata_list:
    #    print(monster_screenshot_metadata)
    '''



    #Regex Lv #
    #Search for monster list monsters in remaining text
    #Regex ##/##/## for date
    #Regex ##:##:## for time
