import pandas as pd
import os
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
import string
import gensim
from random import randint

basePath = os.path.dirname(os.path.abspath(__file__))
full_path = basePath + '/data/goodreads_books_sample.json'

def extract_text_df():
    text_df = pd.DataFrame(columns=['book_id', 'text'])
    lines_with_error_count = 0
    with open(full_path) as json_file:
        for line in json_file:
            try:
                data = json.loads(line)
                book_id = data["book_id"]
                title = data["title"]
                description = data["description"]
                popular_shelves = data["popular_shelves"]
                shelf_text = ""
                for shelf in popular_shelves:
                    if int(shelf["count"]) > 50:
                        shelf_name = shelf["name"]
                        if shelf_name not in ['to-read', 'currently-reading', 'read', 'owned', 'books-i-own',
                                              'kindle', 'audio', 'audiobook', 'to-buy',
                                              'ebook', 'i-own', 'owned-books', 'audiobooks', 'ebooks', 'default',
                                              'library', 'my-library', 'my-ebooks', 'e-book', 'e-books', 'have', 'tbr',
                                              ]:
                            shelf_text += " " + shelf["name"]

                text = title + ' ' + description + ' ' + shelf_text
                if len(text) > 100:
                    text_df = text_df.append({'book_id': book_id, 'text': text}, ignore_index=True)
            except:
                lines_with_error_count += 1
        return text_df


def remove_punctuation(text):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct


def remove_stopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words


def word_stemmer(text):
    stemmer = PorterStemmer()
    stem_text = " ".join([stemmer.stem(i) for i in text])
    return stem_text


def clean_df_text(df):
    df["text"] = df["text"].apply(lambda x: remove_punctuation(x))
    print("punctuation removed...")
    tokenizer = RegexpTokenizer(r'\w+')
    df["text"] = df["text"].apply(lambda x: tokenizer.tokenize(x.lower()))
    print("tokenized...")
    df["text"] = df["text"].apply(lambda x: remove_stopwords(x))
    print("removed stop words...")
    df["text"] = df["text"].apply(lambda x: word_stemmer(x))
    print("stemmed...")
    return df

def compute_book_similarity(book_a, book_b):
    model = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)
    distance = model.wmdistance(book_a, book_b)
    return distance


def main():
    df = extract_text_df()
    print("extracted...")
    print("cleaning starts now...")
    df = clean_df_text(df)
    print("cleaning is complete")
    book1_text = df['text'].iloc[randint(0, df.shape[0]-1)]
    book2_text = df['text'].iloc[randint(0, df.shape[0]-1)]
    print(book1_text)
    print(book2_text)
    distance = compute_book_similarity(book1_text, book2_text)

    print("Similarity score: %.2f" % distance)

if __name__ == "__main__":
    main()


