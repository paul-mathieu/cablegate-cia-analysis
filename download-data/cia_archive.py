from internetarchive import get_item, search_items
from core import *
from pathlib import Path

def download_collection():
    # init variables
    search = search_items('collection:cia-collection')
    data_path = str(Path(__file__).parent.parent.absolute()) + '/data/cia'
    len_search = search.num_found
    index_progression = 0
    errors = 0
    # init progress bar
    print_progress_bar(
        index_progression, len_search,
        prefix = 'Progress:', suffix = 'Complete',
        length = 50)
    # for each article
    for result in search:
        try:
            item = get_item(result['identifier'])
            formats = [e['format'] for e in item.files]
            formats_available = [e for e in formats if 'TXT' in e]
            # download if possible
            if len(formats_available) > 0:
                item.download(
                    formats=formats_available, destdir=data_path,
                    no_directory=True, silent=True)
            # display progression
            index_progression += 1
            if round(index_progression/len_search, 3)%.001 == 0: # each .1%
                print_progress_bar(
                    index_progression, len_search,
                    prefix = 'Progress:', suffix = 'Complete',
                    length = 50)
        except:
            # if error
            errors += 1
    print(errors, ' errors')
