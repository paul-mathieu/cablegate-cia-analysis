#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
nlp.vocab["CLASSIFIED"].is_stop = True # On ajoute CLASSIFIED au stop words


# In[20]:


data_path = './echantillon-cablegate_converted/'
files = [f for f in listdir(data_path) if f[-4:] == '.txt']
files.sort()


# In[21]:


files


# In[44]:


def extract_subject(content):
    subject_pos = content.index('\nSUBJECT: ') + len('\nSUBJECT: ') 
    subject = content[subject_pos: subject_pos + 500]
    try:
        end_pos = subject.index('\n \n')
    except:
        end_pos = subject.index('\n')
    subject = subject[:end_pos].replace('\n', ' ')
    return subject


# In[50]:


def extract_date(content, filename):
    date_line = re.search(r"[A-Z]\s[0-9]{6}[A-Z]\s[A-Z]{3}\s[0-9]{2}", content)
    if date_line == None:
        if int(filename[0:2]) > int(current_year):
            year = "19"+filename[0:2]
        else:
            year="20"+filename[0:2]
        return {'year':year}
    
    date_line = date_line.group()
    date_month = date_line.split(" ")[2]
    date_year = date_line.split(" ")[3]
    
    months = ['JAN', 'FEB', 'MAR', "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    date = {}
    date['year'] = None
    date['month'] = None
    if date_month in months :
        if int(date_year) > int(current_year):
            year = "19"+date_year
        else:
            year="20"+date_year
        date['year'] = year
        date['month'] = date_month
    else :
        print("ERR : unexpected month =", date_month)
    return date


# In[47]:


def extract_tags(content):
    try:
        tag_pos = content.index('\nTAGS: ') + len('\nTAGS: ')
    except:
        tag_pos = content.index('\nTAGS ') + len('\nTAGS ')
    tags = content[tag_pos: tag_pos + 500]
    end_pos = tags.index('\n')
    tags = tags[:end_pos].replace(',', '')
    return tags.split(' ')


# In[8]:


def extract_from(content):
    #fm_list = [line for line in content.splitlines() if line.startswith("FM ")]
    #return fm_list[0][3:-1] # y a toujours un espace à la fin
    FROM = re.search(r"\nFM\s[A-Z\s]+\nTO ", content)
    if FROM != None :
        FROM = FROM.group()[4:-4]
    else:
        #print(re.search(r"\nFOR\s[A-Z\/s]+", content))
        FROM = re.search(r"\nFOR\s[A-Z\s\/]+\n", content)
        if FROM != None :
            FROM = FROM.group()[5:-1]
            FROM =re.split(', | AND ',FROM)
    return FROM


# In[9]:


def extract_most_common_words(content):
    doc = nlp(content)
    # all tokens that arent stop words or punctuations
    words = [token.text for token in doc if not token.is_stop and not token.is_punct and token.text not in ("\n", "\n \n", "\n \n \n")]

    # fiftenth most common tokens
    word_freq = Counter(words)
    common_words = word_freq.most_common(15)
    return [word for word in common_words if len(word[0])>1]


# In[10]:


def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.is_stop or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5


# In[11]:


def extract_keywords(content):
    output = set(get_hotwords(content))
    return [x[0] for x in Counter(output).most_common(5)]


# In[12]:


def extract_entity_involved(ner):
    entity_involved = [key.replace('\n', '').replace('   ', ' ').replace('  ',' ') for key in ner.keys() if ner[key] == 'ORG' or ner[key] == 'NORP' ]
    res = []
    for entity in entity_involved: # to remove duplicates
        if entity not in res:
            res.append(entity)
    return res 


# In[28]:


def extract_place_involved(ner):
    place_involved = [key
                      .replace('\n', '')
                      .replace('   ', ' ')
                      .replace('  ', ' ')
                      .upper()
                      for key in ner.keys() if ner[key] == 'GPE' or ner[key] == 'LOC' ]
    res = []
    for place in place_involved: # to remove duplicates
        if place[0:4]=="THE " and len(place)>4:
                place = place.replace("THE ", "")
        if place not in res:
            res.append(place)
    return res 


# In[14]:


def extract_people_involved(ner): # on laisse sipdis parce que peut être une personne
    people_involved = [key.replace('\n', '').replace('   ', ' ').replace('  ', ' ') for key in ner.keys() if ner[key] == 'PERSON']
    res = []
    for people in people_involved: # to remove duplicates
        if people not in res:
            res.append(people)
    return res 


# In[56]:


# Cleaning

res = {}
current_filename = re.search(r"[0-9][0-9][A-Z]+", files[0]).group()
end = len(files)
t = time.time()
for i in range(0, end):
    with open(data_path + files[i], encoding="utf8", errors='ignore') as f:
        content = f.read()
        if content != "":
            filename = re.search(r"[0-9][0-9][A-Z]+", files[i]).group()
            if filename != current_filename:
                with open('./output/'+current_filename + ".json", "w") as out_file: # On écrit dans le fichier
                    json.dump(res, out_file)

                current_filename = filename
                
                res = {}

            extracted_doc = {}
            
            doc_name =  files[i][:-4]
            extracted_doc['date'] = extract_date(content, filename)
            extracted_doc['tags'] = extract_tags(content)
            extracted_doc['from'] = extract_from(content)
            extracted_doc['place_of_document'] = re.findall(r"[A-Z]+", doc_name)[-1] # -1 because we take the last one
            extracted_doc['subject'] = extract_subject(content)
            extracted_doc['most_common_words'] = extract_most_common_words(content)
            extracted_doc['keywords'] = extract_keywords(content)

            ner = dict([(str(x), x.label_) for x in nlp(content).ents])
            extracted_doc['people_involved'] = extract_people_involved(ner)
            extracted_doc['place_involved'] = extract_place_involved(ner)
            extracted_doc['entity_involved'] = extract_entity_involved(ner)

            print_progress_bar(i, end, prefix = 'Progress:', suffix = 'Complete', length = 50)

            res[doc_name] = extracted_doc

print(round(t - time.time(), 2))


# In[15]:


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


# In[ ]:




