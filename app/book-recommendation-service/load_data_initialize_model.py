import os
import csv
import torch
from models import InferSent
import utils

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

this_dir = os.path.dirname(__file__)
# global data structures
similar_books_map = {}
book_id_descriptions = {}
book_id_titles = {}
book_id_map = {}

# load similar book csv as a global - only read once at service startup time
with open(os.path.join(this_dir, "data/book_id_map.csv"), mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)
    book_id_map = {rows[0]: rows[1] for rows in reader}

with open(os.path.join(this_dir, "data/similar_books.csv"), mode='r') as infile:
    reader = csv.reader(infile)
    # skip header line
    next(reader)
    similar_books_map = {rows[0]: utils.extract_list_from_string(rows[1]) for rows in reader}

# add supplemental similar book list
with open(os.path.join(this_dir, "data/book_to_similar_books.csv"), mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)
    for rows in reader:
        book_id_csv = rows[0]
        # convert csv book id to goodreads book_id
        if book_id_csv in book_id_map:
            actual_book_id = book_id_map[book_id_csv]
            if actual_book_id in similar_books_map:
                # combine similar books, removing duplicates with set
                try:
                    new_books_to_add = list(utils.extract_list_from_string(rows[1]))
                    similar_books_map[actual_book_id] = set(similar_books_map[actual_book_id]
                                                            + utils.convert_book_ids_to_goodreads_id(new_books_to_add,
                                                                                                     book_id_map))
                except:
                    continue
            else:
                similar_books_map[actual_book_id] = utils.convert_book_ids_to_goodreads_id(
                    utils.extract_list_from_string(rows[1]), book_id_map)


with open(os.path.join(this_dir, "data/description.csv"), mode='r') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        if len(rows[1]) > 20:
            book_id_descriptions[rows[0]] = rows[1]

with open(os.path.join(this_dir, "data/title.csv"), mode='r') as infile:
    reader = csv.reader(infile)
    next(reader)
    book_id_titles = {rows[0]: rows[1] for rows in reader}


model_path = "encoder/infersent2.pkl"
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                    'pool_type': 'max', 'dpout_model': 0.0, 'version': 2}
model = InferSent(params_model)
model.load_state_dict(torch.load(model_path))

w2v_path = 'fastText/crawl-300d-2M.vec'
model.set_w2v_path(w2v_path)

# Load embeddings of K most frequent words
model.build_vocab_k_words(K=100000)
