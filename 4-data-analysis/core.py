from pathlib import Path
from time import strftime, gmtime
from difflib import SequenceMatcher
import requests





PROJECT_PATH = str(Path(__file__).parent.parent.absolute()).replace('\\', '/')
LOCAL_PATH = str(Path(__file__).parent.absolute()).replace('\\', '/')
DATA_PATH = PROJECT_PATH + '/data'

# Print iterations progress
def print_progress_bar(iteration, total,
                    prefix = '', suffix = '',
                    decimals = 1, length = 100,
                    fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def duration_formater(duration):
    return strftime('%H:%M:%S', gmtime(duration))


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
        # print(place)
        country = place.split(", ")[-1]
        return country
    except:
        return None
