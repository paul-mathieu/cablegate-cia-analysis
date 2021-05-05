# try:
#     from PIL import Image
# except ImportError:
#     import Image

import pytesseract

from pdf2image import convert_from_path
from core import *
from pathlib import Path
from os import listdir


def convert_data(local_path=LOCAL_PATH):
    data_path = local_path + '/data/cia/'
    converted_data_path = local_path + '/data/cablegate-converted/'
    files = [f for f in listdir(data_path) if f[-4:] == '.pdf']
    print(files)
    index_progression = 0
    print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        txt_file = open(converted_data_path + file[:-4] + '.txt', 'w')
        txt_file.write(pdf_to_string(data_path + file))
        txt_file.close()
        index_progression += 1
        print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)

    print(data_path)

def pdf_to_string(file_path):
    pages = convert_from_path(file_path, 300)
    print(pages)
    text = ''
    for page_num, img_blob in enumerate(pages):
        text += pytesseract.image_to_string(img_blob, lang='eng')

    return text
