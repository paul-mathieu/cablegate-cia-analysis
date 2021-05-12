#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import listdir
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# In[2]:


data_path = './output/'
files = [f for f in listdir(data_path) if f[-5:] == '.json']
files.sort()


# In[13]:


# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off");


# In[14]:


for file in files:
    current_file = open(data_path + file, encoding="utf8", errors='ignore')
    content = json.load(current_file)
    current_file.close()
    
    d = {}
    if content !={} :
        for key in content.keys():
            for word in content[key]['most_common_words']:
                word_transformed = word[0].upper().replace("'", " ")
                if word_transformed in d.keys():
                    d[word_transformed] = d[word_transformed] + int(word[1])
                else : 
                    d[word_transformed] = int(word[1])

        wordcloud = WordCloud(width=3000,height=2000, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(d)
        plot_cloud(wordcloud)

        break


# In[ ]:




