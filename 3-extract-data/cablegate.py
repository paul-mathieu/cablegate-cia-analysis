import json
import requests

from cablegatedata import *
from difflib import SequenceMatcher
from pathlib import Path
from os import listdir


def get_country_from_api(place):
    # return country or None
    data = requests.get(
        'https://nominatim.openstreetmap.org/search?q="{}"&format=json&accept-language=en'.format(place)).json()
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
    if place in correspondance_dict.keys():
        return correspondance_dict[place], True

    # if similar place was searched
    for correspondance_place in correspondance_dict.keys():
        if SequenceMatcher(None, place, correspondance_place).ratio() > .9:
            return correspondance_place, False

    # if place wasn't searched
    return get_country_from_api(place), False


def display():
    print(get_country('BORDEAUX'))


def extract_data(data_dict=res):
    output_dict = None

    # extract correspondence dict
    file = open('../data/cablegate-for-analysis/correspondence-dict.json', 'r')
    correspondence_dict = json.load(file)
    file.close()

    # files list
    files_dir = '../data/cablegate-for-analysis/summary/'
    files_path = [f for f in listdir(files_dir) if f[-4:] == '.json']

    for file_path in files_path:
        file = open(files_dir + file_path, 'r')
        data_dict = json.load(file)
        # for each document data
        for document_name in data_dict.keys():
            # if no output dict yet
            if output_dict is None:
                actual_country, = get_country(data_dict[], correspondence_dict)
                if actual_country is not None:
                    output_dict = {actual_country: []}
            # if output dict created
            if output_dict is not None:
                for place in data_dict[document_name]['place_involved']:
                    country_from_place = get_country(place, correspondence_dict)
                    # if place was found
                    if place is not None:
                        output_dict[actual_country].append(country_from_place[0])
                        # if place doesn't exist yet in correspondence dict
                        if country_from_place[1]:
                            correspondence_dict[place] = country_from_place[0]
        file.close()

    # export correspondance dict
    file = open('../data/analysis/correspondence-dict.json', 'w')
    json.dump(correspondence_dict, file)
    file.close()

    return output_dict

# def link_countries(doc):
#     link = {} # ex: {'france': {'espagne':3, ...}, 'belgique': {'espagne':2, ...}, ...}
#     country_from = get_country_from(doc)
#     places_involved = doc['place_involved']
#     for place in places_involved:
#         if place in countries : # si la place est un pays (il faut bien transformer la place)
#             if place in link[country_from].keys(): # si le pays est déjà dans le lien
#                 link[country_from][place] += 1
#             else : # si le pays n'est dans le lien
#                 link[country_from][place] = 1
#         else:
#             # si la place n'est pas un pays, on cherche le pays de la place
#             if place in place_to_country: # on vérifie si la place a déjà une correspondance à un pays dans le fichier
#                 #blabla
#                 country = place_to_country[place]
#                 link[country_from][]
#             else:
#                 country_of_place_involved = get_country(place)
#                 # on ecrit la correspondance de la place dans un fichier
#
#             # pour économiser des requetes, on stocke la correspondance des lieu pour voir si on a déjà fait la
#             # requête
#     link[country_from]
#     countries_to = get_country
