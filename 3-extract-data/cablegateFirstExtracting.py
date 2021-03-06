import re
import spacy
from collections import Counter
from string import punctuation
from os import listdir
import time
import pprint
import json

current_year = time.strftime("%y", time.localtime())

nlp = spacy.load('en_core_web_lg')
nlp.vocab["CLASSIFIED"].is_stop = True  # On ajoute CLASSIFIED au stop words


data_path = './data/cablegate-converted/'
files = [f for f in listdir(data_path) if f[-4:] == '.txt']
files.sort()

def extract_subject(text):
    try:
        subject_pos = text.index('\nSUBJECT: ') + len('\nSUBJECT: ')
        subject = text[subject_pos: subject_pos + 500]
        try:
            if '\n \n' in subject:
                return subject[:subject.index('\n \n')].replace('\n', ' ')
            if '\n\n' in subject:
                return subject[:subject.index('\n\n')].replace('\n', ' ')
            if '\n' in subject:
                return subject[:subject.index('\n')].replace('\n', ' ')
        except:
            return ''
    except:
        return ''

def extract_date(text, file_name):
    date_line = re.search(r"[A-Z]\s[0-9]{6}[A-Z]\s[A-Z]{3}\s[0-9]{2}", text)
    if date_line is None:
        if int(file_name[:2]) > 50:
            return {'year': "19" + file_name[:2]}
        else:
            return {'year': "20" + file_name[:2]}

    date_line = date_line.group()
    date_month = date_line.split(" ")[2]
    date_year = date_line.split(" ")[3]

    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    date = {'year': None, 'month': None}
    if date_month in months:
        if int(date_year) > 50:
            date['year'] = "19" + date_year
        else:
            date['year'] = "20" + date_year
        date['month'] = date_month
    # else:
    #     print("ERR : unexpected month =", date_month)
    return date

def extract_tags(text):
    if 'TAGS:' in text:
        try:
            tag_pos = text.index('\nTAGS: ') + 7  # len('\nTAGS: ')
        except:
            tag_pos = text.index('TAGS: ') + 6
    elif 'TAGS' in text:
        try:
            tag_pos = text.index('\nTAGS ') + 6  # len('\nTAGS ')
        except:
            return []
    else:
        return []
    tags = text[tag_pos: tag_pos + 500]
    
    if '\n' in tags:
        return tags[:tags.index('\n')].replace(',', '').split(' ')
    else:
        return []
    

def extract_from(text):
    # fm_list = [line for line in content.splitlines() if line.startswith("FM ")]
    # return fm_list[0][3:-1] # y a toujours un espace ?? la fin
    fm = re.search(r"\nFM\s[A-Z\s]+\nTO ", text)
    if fm is not None:
        return fm.group()[4:-4]
    else:
        fm = re.search(r"\nFOR\s[A-Z\s/]+\n", text)
        if fm is not None:
            return re.split(', | AND ', fm.group()[5:-1])
        else:
            return ''

def extract_most_common_words(text):
    doc = nlp(text)
    # all tokens that arent stop words or punctuations
    words = [token.text for token in doc if
             not token.is_stop and not token.is_punct and token.text not in ("\n", "\n \n", "\n \n \n")]
    # fiftenth most common tokens
    return [word for word in Counter(words).most_common(15) if len(word[0]) > 1]


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN']  # 1
    doc = nlp(text.lower())  # 2
    for token in doc:
        # 3
        if token.is_stop or token.text in punctuation:
            continue
        # 4
        if token.pos_ in pos_tag:
            result.append(token.text)

    return result  # 5


def extract_keywords(text):
    return [x[0] for x in Counter(set(get_hotwords(text))).most_common(5)]

def extract_entity_involved(ner):
    entity_involved = [key.replace('\n', '').replace('   ', ' ').replace('  ', ' ')
                       for key in ner.keys() if ner[key] == 'ORG' or ner[key] == 'NORP']
    result = []
    for entity in entity_involved:  # to remove duplicates
        if entity not in result:
            result.append(entity)
    return result  # mieux set g??n??rateur


def extract_place_involved(ner):
    place_involved = [key.replace('\n', '').replace('   ', ' ').replace('  ', ' ').upper()
                      for key in ner.keys() if ner[key] == 'GPE' or ner[key] == 'LOC']
    result = []
    for place in place_involved:  # to remove duplicates
        if place[0:4] == "THE " and len(place) > 4:
            place = place.replace("THE ", "")
        if place not in result:
            result.append(place)
    return result


def extract_people_involved(ner):  # on laisse sipdis parce que peut ??tre une personne
    people_involved = [key.replace('\n', '').replace('   ', ' ').replace('  ', ' ') for key in ner.keys() if
                       ner[key] == 'PERSON']
    result = []
    for people in people_involved:  # to remove duplicates
        if people not in result:
            result.append(people)
    return result  # mieux set g??n??rateur

# Print iterations progress
def print_progress_bar(iteration, total,
                       prefix='', suffix='',
                       decimals=1, length=100,
                       fill='???', printEnd="\r"):
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
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

res = {}
current_filename = re.search(r"[0-9][0-9][A-Z]+", files[0]).group()
nb_files = len(files)
t = time.time()
# initialise la progress bar
i = 0
print_progress_bar(i, nb_files, prefix='Progress:', suffix='Complete', length=50)

files_data = {}

start = False
for file in files:
    if re.search(r"[0-9][0-9][A-Z]+", file).group() == "07BUDAPEST":
        start = True
    if start:
        current_file = open(data_path + file, encoding="utf8", errors='ignore')
        content = current_file.read()
        current_file.close()

        if content != "":
            filename = re.search(r"[0-9][0-9][A-Z]+", file).group()
            if filename != current_filename:
                out_file = open('./output/' + current_filename + ".json", "w")  # On ??crit dans le fichier
                json.dump(files_data, out_file)
                out_file.close()

                current_filename = filename

                files_data = {}

            doc_name = file[:-4]
            ner = dict([(str(x), x.label_) for x in nlp(content).ents])

            files_data[doc_name] = {'date': extract_date(content, filename),
                                    'tags': extract_tags(content),
                                    'from': extract_from(content),
                                    'place_of_document': re.findall(r"[A-Z]+", doc_name)[-1],
                                    # -1 because we take the last one
                                    'subject': extract_subject(content),
                                    'most_common_words': extract_most_common_words(content),
                                    'keywords': extract_keywords(content),
                                    'people_involved': extract_people_involved(ner),
                                    'place_involved': extract_place_involved(ner),
                                    'entity_involved': extract_entity_involved(ner)}

    i += 1
    #if i == 1000:
    #break
    if i % 1000 == 0:
        print_progress_bar(i, nb_files, prefix='Progress:', suffix='Complete', length=50)

print(round(t - time.time(), 2))