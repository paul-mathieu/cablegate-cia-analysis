from pathlib import Path
from tika import parser
from os import listdir
from core import *
from privar import *
import re
import time
# from boto3.session import Session
import boto3


def convert_data(download_files=False, upload_files=True, local_path=LOCAL_PATH):
    # variables
    path_source = str(Path(__file__).parent.parent.absolute()).replace('\\', '/')
    data_path = path_source + '/data/cablegate/'
    data_path = 'C:/Users/paul-/Desktop/Polytech/8_PROJ831/data/cablegatepdf/'
    converted_data_path = path_source + '/data/cablegate-converted/'
    files = [f for f in listdir(data_path) if f[-4:] == '.pdf']
    len_files = len(files)
    # connexion to boto3
    client = boto3.client(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2')
    # replacement of bad syntax
    replace_dict = {
        '\n\n\n': '',
        '\n\n': '\n',
        'S E C R E T': 'SECRET',
        'C O N F I D E N T I A L': 'CONFIDENTIAL',
        '[INFORMATION FOR THE REPORT\'S CLASSIFIED ANNEX]': '',
        '[INFORMATION FOR THE REPORT\'S CLASSIFIED ANNEX.]': '',
        'This record is a partial extract of the original cable. The full text of the original cable is not available.': ''
        }
    re_compile = re.compile("(%s)" % "|".join(map(re.escape, list(replace_dict.keys())[:-1])))
    # init time compilation
    start_time = time.time()
    # progress bar
    index_progression = 0
    print_progress_bar(index_progression, len_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        # get txt from pdf
        text = parser.from_file(data_path + file)['content']
        # remove all before start code if possible
        if 'vzczc' in text:
            text = text[text.index('vzczc'):]
        # if files need to be downloaded
        if download_files:
            # write new file
            with open(converted_data_path + file[:-3] + 'txt', 'w') as f:
                # f.write(re_compile.sub(lambda mo: replace_dict[mo.string[mo.start(): mo.end()]], text))
                try:
                    f.write(
                        re_compile.sub(
                            lambda mo: replace_dict[mo.string[mo.start(): mo.end()]],
                            re.sub('\/tag\/\w{3,8}.html', '',text)
                        )
                    )
                except UnicodeEncodeError: # if charcacter errors
                    f.write(
                        re_compile.sub(
                            lambda mo: replace_dict[mo.string[mo.start(): mo.end()]],
                            re.sub('\/tag\/\w{3,8}.html', '',text)
                        ).encode('ascii', 'ignore').decode()
                    )
            # if files need to be uploaded
            if upload_files:
                client.put_item(
                    TableName='cablegate_document',
                    Item={
                        'name': {'S': file[:-4]},
                        'content': {'S': re_compile.sub(
                        lambda mo: replace_dict[mo.string[mo.start(): mo.end()]],
                        text)}
                    }
                )
        index_progression += 1
        if index_progression%250 == 0:
            print_progress_bar(index_progression, len_files,
                prefix = 'Progress:',
                suffix = str(index_progression) + ' files converted in ' + duration_formater(time.time() - start_time),
                length = 50)

    print(time.time() - start_time)


def test():
    session = Session(
        # 'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-east-2')
    client = session.client('dynamodb')

    client.put_item(
        TableName='cablegate_document',
        Item={'name': {'S': 'test_file_1'}, 'content':{'S': 'test'}}
        # Item={'name': {'S': 'test_file_1'}, 'content':{'S': 'test'}}
    )

def test2():
    client = boto3.client('dynamodb',aws_access_key_id='AKIA4TXQL45ERJQKPIY4', aws_secret_access_key='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', region_name='us-east-2')
    client.put_item(
        TableName='cablegate_document',
        Item={
            'name':{'S': 'nom_du_document_paul2'},
            'content':{'S': 'contenu_du_document_paul2'}
        }
    )




#
