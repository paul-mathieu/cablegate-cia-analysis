from pathlib import Path
from tika import parser
from os import listdir
from core import *
import time

def convert_data():
    # variables
    path_source = str(Path(__file__).parent.parent.absolute()).replace('\\', '/')
    data_path = path_source + '/data/cablegate/'
    converted_data_path = path_source + '/data/cablegate-converted/'
    files = [f for f in listdir(data_path) if f[-4:] == '.pdf']
    # start_time = time.time()
    index_progression = 0
    print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        txt_file = open(converted_data_path + file[:-4] + '.txt', 'w')
        txt_file.write(parser.from_file(data_path + file)['content'].replace('\n\n\n','').replace('\n\n','\n'))
        txt_file.close()
        index_progression += 1
        print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
        # print(time.time() - start_time)
