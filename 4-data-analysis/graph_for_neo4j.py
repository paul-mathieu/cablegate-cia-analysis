#!/usr/bin/env python
# coding: utf-8

# In[1]:


from os import listdir
import json
# import the neo4j driver for Python
from neo4j import GraphDatabase
from collections import Counter


# # Connection configuration

# In[2]:


# Database Credentials
uri             = "bolt://localhost:7687"
userName        = "username"
password        = "password"

# Connect to the neo4j database server
graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))


# In[3]:


data_path = './output/'
files = [f for f in listdir(data_path) if f[-5:] == '.json']
files.sort()


# In[4]:


files[0][2:-5] + files[0][0:2]


# # Query

# In[17]:


def create_node(node_name, name, node_type):
    return "CREATE (" + node_name + ":" + node_type + "{ name:'" + name + "'})"


# In[18]:


def create_node_if_needed(node_name, name,node_type, session):
    exist_query = "MATCH (n) WHERE n.name ='" + name + "'RETURN n"
    res = session.run(exist_query)
    if len(res.value())==0: # doesn't exist
        session.run(create_node(node_name, name, node_type))


# In[19]:


def create_relationship_between_existing_nodes(name1,relation_type,name2):
    return "MATCH (n), (m) WHERE n.name = '" + name1 + "' AND m.name = '" + name2 + "' CREATE (n)-[:" + relation_type + "]->(m)"


# In[20]:


def create_relationship(node1_name, name1, node1_type, relation_type, node2_name, name2, node2_type, session):
    '''
    Create a relationship between 2 nodes by creating them if necessary
    '''
    
    # We use the node_name to identify a node
    create_node_if_needed(node1_name, name1, node1_type, session)
    create_node_if_needed(node2_name, name2, node2_type, session)
    return session.run(create_relationship_between_existing_nodes(name1,relation_type,name2))


# # Process

# In[9]:


session = graphDB_Driver.session()


# In[46]:


i_ent = 0
i_per = 0
i_doc = 0
i=0
for file in files:
    current_file = open(data_path + file, encoding="utf8", errors='ignore')
    content = json.load(current_file)
    current_file.close()
    
    if content != {} :
        doc_node_name = file[2:-5] + file[0:2]
        print(doc_node_name)
        
        people = []
        entities = []
        text_dict = {}
        for key in content.keys():
            people_transformed = [people.upper().replace("'", " ") for people in content[key]['people_involved'] ]
            people.extend(people_transformed)
            entity_transformed = [entity.upper().replace("'", " ") for entity in content[key]['entity_involved'] ]
            entities.extend(entity_transformed)
            
            text_dict[key] = {}
            text_dict[key]['people'] = people_transformed
            text_dict[key]['entity'] = entity_transformed
        
        people_duplicates = [p for p in people if people.count(p) == 3] # ils sont chacun mentionnés au moins dans 3 textes
        entity_duplicates = [e for e in entities if entities.count(e) == 3] # ils sont chacun mentionnés dans au moins 4 textes 
        

        people_mentioned_in_different_document = list(set(people_duplicates)) # sans les doublons
        entities_mentioned_in_different_document = list(set(entity_duplicates)) # sans les doublons
        
        people_mentioned_in_different_document = people_mentioned_in_different_document[0:10] # on limite à 10
        entities_mentioned_in_different_document = entities_mentioned_in_different_document[0:10] # on limite à 10
        print(len(people_mentioned_in_different_document))
        print(len(entities_mentioned_in_different_document))
        
        for key in text_dict.keys():
            for people in people_mentioned_in_different_document:
                if people in text_dict[key]['people']:
                    create_relationship('p' + str(i_per), people, 'person', 'mentioned', 'd' + str(i_doc), key, 'doc', session)
                    i_per += 1
                
            for entity in entities_mentioned_in_different_document:
                if entity in text_dict[key]['entity']:
                    create_relationship('e' + str(i_ent), entity, 'entity', 'mentioned', 'd' + str(i_doc), key, 'doc', session)
                    i_ent += 1
            
            i_doc += 1


            
    
        
        #i = i+1
        #if i==5:
        break


# In[ ]:




