import json
import requests
import time
from core import *
from cablegatedata import *
from difflib import SequenceMatcher
from pathlib import Path
from os import listdir


def get_country_from_api(place):
    # return country or None
    try:
        data = requests.get(
            'https://nominatim.openstreetmap.org/search'
            '?q="{}"&format=json&accept-language=en'.format(place)).json()
    except ConnectionError:
        print('Error with: ', place)
    try:
        place = data[0]['display_name']
        country = place.split(", ")[-1]
        if country in countries:
            return country
        else:
            for country_name in countries:
                if SequenceMatcher(None, country, country_name).ratio() > .9:
                    return country_name
            return None
    except:
        return None


def get_country(place, correspondance_dict):
    # return country and presence in correspondance_dict
    # if place was searched
    if place in list(correspondance_dict.keys()):
        return correspondance_dict[place], True

    # if similar place was searched
    for correspondance_place in list(correspondance_dict.keys()):
        if SequenceMatcher(None, place, correspondance_place).ratio() > .9:
            return correspondance_place, False

    # if place wasn't searched
    return get_country_from_api(place), False

def display():
    print(DATA_PATH)
    try:
        file = open(DATA_PATH + '/analysis/correspondence-dict.json', 'r')
        correspondence_dict = json.load(file)
        file.close()
    except FileNotFoundError:
        correspondence_dict = {}
    print(get_country('UNITED D STATES', correspondence_dict))
    # print(list(correspondence_dict.values()))
    # for e in correspondence_dict.keys():
    #     if correspondence_dict[e] is not None:
    #         if correspondence_dict[e] == correspondence_dict[e].upper():
    #             print({e: correspondence_dict[e]})

def extract_data(data_dict=res):
    output_dict = {}
    actual_country = 'unknown'
    actual_country_raw = None

    # extract correspondence dict
    try:
        file = open(DATA_PATH + '/analysis/correspondence-dict.json', 'r')
        correspondence_dict = json.load(file)
        file.close()
    except FileNotFoundError:
        correspondence_dict = {}

    # files list
    files_dir = DATA_PATH + '/cablegate-for-analysis/summary/'
    files_path = [f for f in listdir(files_dir) if f[-5:] == '.json']
    # print(files_path)

    for file_path in files_path:
        print('file name: ', file_path)
        file = open(files_dir + file_path, 'r')
        data_dict = json.load(file)
        # progress bar
        len_files = len(list(data_dict.keys()))
        start_time = time.time()
        index_progression = 0
        print_progress_bar(index_progression, len_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
        # for each document
        for document_name in list(data_dict.keys()):
            # if new country
            if actual_country_raw != data_dict[document_name]['place_of_document']:
                actual_country_raw = data_dict[document_name]['place_of_document']
                actual_country, _ = get_country(actual_country_raw, correspondence_dict)
                if actual_country is not None:
                    if actual_country == actual_country.upper():
                        actual_country, _ = get_country(country_from_place[0], correspondence_dict)
                # print('actual_country_raw: ', actual_country_raw)
                # print('actual_country: ', actual_country)
                output_dict[actual_country] = {}

            for place in data_dict[document_name]['place_involved']:
                country_from_place = get_country(place, correspondence_dict)
                if country_from_place[0] is not None:
                    if country_from_place[0] == country_from_place[0].upper():
                        country_from_place = get_country(country_from_place[0], correspondence_dict)
                # print(place, country_from_place)
                # if place was found
                if place is not None:
                    if country_from_place[0] in output_dict[actual_country].keys():
                        output_dict[actual_country][country_from_place[0]] += 1
                    else:
                        output_dict[actual_country][country_from_place[0]] = 1

                    # if place doesn't exist yet in correspondence dict
                    if not country_from_place[1]:
                        correspondence_dict[place] = country_from_place[0]

            index_progression += 1
            print_progress_bar(index_progression, len_files,
                prefix = 'Progress:',
                suffix = str(index_progression) + ' files converted in ' + duration_formater(time.time() - start_time),
                length = 50)


        file.close()
        # export countries count
        file_save = open(DATA_PATH + '/analysis/save-dict.json', 'w')
        json.dump(output_dict, file_save)
        file_save.close()
        # export correspondance dict
        file = open(DATA_PATH + '/analysis/correspondence-dict.json', 'w')
        json.dump(correspondence_dict, file)
        file.close()

    return output_dict

def reformat_country_names():
    file = open(DATA_PATH + '/analysis/save-dict.json', 'r')
    data = json.load(file)
    file.close()

    file = open(DATA_PATH + '/analysis/correspondence-dict.json', 'r')
    correspondence_dict = json.load(file)
    file.close()

    errors = [e for e in list(data.keys()) if e.upper() == e]
    corrections = {e: get_country(e, correspondence_dict)[0] for e in errors}

    for country in list(data.keys()):
        if country in errors:
            print(corrections[country])
            data[corrections[country]] = data[country]
            data.pop(country)

    file_save = open(DATA_PATH + '/analysis/save-dict.json', 'w')
    json.dump(data, file_save)
    file_save.close()
