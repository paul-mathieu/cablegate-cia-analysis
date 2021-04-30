from pathlib import Path
from tika import parser
from os import listdir
from core import *
import re
import time

def convert_data(local_path=LOCAL_PATH):
    # variables
    path_source = str(Path(__file__).parent.parent.absolute()).replace('\\', '/')
    data_path = path_source + '/data/cablegate/'
    converted_data_path = path_source + '/data/cablegate-converted/'
    files = [f for f in listdir(data_path) if f[-4:] == '.pdf']
    len_files = len(files)
    replace_dict = {
        '\n\n\n': '',
        '\n\n':'\n',
        'S E C R E T': 'SECRET',
        'C O N F I D E N T I A L': 'CONFIDENTIAL',
        '[INFORMATION FOR THE REPORT\'S CLASSIFIED ANNEX]': '',
        '[INFORMATION FOR THE REPORT\'S CLASSIFIED ANNEX.]': ''
        }
    re_compile = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
    start_time = time.time()
    index_progression = 0
    print_progress_bar(index_progression, len_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        text = re_compile.sub(
                    lambda mo: replace_dict[mo.string[mo.start(): mo.end()]],
                    parser.from_file(data_path + file)['content'])
        index_progression += 1
        print_progress_bar(index_progression, len_files, prefix = 'Progress:', suffix = 'Complete', length = 50)

    print(time.time() - start_time)
