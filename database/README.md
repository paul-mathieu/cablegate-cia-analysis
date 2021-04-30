# Basic command to interact with dynamoDB

## Upload and get -> Document
### Upload

```python
# Upload to Cablegate_document
response = client.put_item(
    TableName='cablegate_document',
    Item={
        'name':{'S': 'nom_du_document'} # -> clé
        'content':{'S': 'contenu_du_document'}
    }
)
```

```python
# Upload to cia_document
response = client.put_item(
    TableName='cia_document',
    Item={
        'name':{'S': 'nom_du_document'}, # -> clé
        'content':{'S': 'contenu_du_document'}
    }
)
```
### Get
```python
# Read from Cablegate_document
response = client.get_item(
    Key={
        'name': {'S': 'nom_du_document'}
    },
    TableName='cablegate_document'
)
```
```python
# Read from cia_document
response = client.get_item(
    Key={
        'name': {'S': 'nom_du_document'}
    },
    TableName='cia_document'
)
```

## Upload and get -> Document_transformed(BD)
### Upload
```python
# Upload to cablegate_document_transformed
response = client.put_item(
    TableName='cablegate_document_transformed',
    Item={
        'name': {'S': 'nom_du_document'}, # -> clé
        'subject':{'S': 'sujet_du_document'},
        'tags':{'SS' : ['tag1', 'tag2']}, # -> list
        'people_involved' : {'SS' : ['person1', 'person2']},
        'document_location' : {'S': 'sujet_du_document'},
        'countries_involved' : {'SS' : ['country1', 'country2']},
        'cities_involved' :{'SS' : ['city1', 'city2']},
        'date' : {'S': 'date_du_document'},
        'entities_involved' : {'SS' : ['entity1', 'entity2']},
        'topic' : {'S': 'theme_du_document'},
        'keywords' :{'SS' : ['keyword1', 'keyword2']}
    }
)
```

```python
# Upload to cia_document_transformed
response = client.put_item(
    TableName='cia_document_transformed',
    Item={
        'name': {'S': 'nom_du_document'}, # -> clé
        'people' : {'SS' : ['person1', 'person2']},
        'date' : {'S': 'date_du_document'},
    }
)
```
### Get
```python
# get from cablegate_document_transformed
response = client.get_item(
    Key={
        'name': {'S': 'nom_du_document'}
    },
    TableName='cablegate_document_transformed'
)
```
```python
# get from cia_document_transformed
response = client.get_item(
    Key={
        'name': {'S': 'nom_du_document'}
    },
    TableName='cia_document_transformed'
)
```
