import pandas as pd
import os
import json
import glob
from random import randint
from sentence_transformers import SentenceTransformer
import scipy

this_dir = os.path.dirname(__file__)
rel_data_path = "../data/goodreads_books_sample.json"
abs_data_path = os.path.join(this_dir, rel_data_path)

def extract_text_df():
    text_df = pd.DataFrame(columns=['book_id', 'text'])
    lines_with_error_count = 0
    with open(abs_data_path) as json_file:
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
                if len(text) > 50:
                    text_df = text_df.append({'book_id': book_id, 'text': text}, ignore_index=True)
            except:
                lines_with_error_count += 1
        return text_df

def generate_embeddings_and_compute_ranked_distance(book_text, similar_book_texts, closest_n):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    book_embedding = model.encode(book_text)
    similar_books_embeddings = model.encode(similar_book_texts)
    distances = scipy.spatial.distance.cdist(book_embedding, similar_books_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("======================\n\n")
    print("Original book:", book_text[0:50], "...")
    print("\nTop " + str(closest_n) + " most similar books:")

    for idx, distance in results[0:closest_n]:
        print(similar_book_texts[idx].strip()[0:50], "... ",  "(Score: %.4f)" % (1 - distance))


def main():
    df = extract_text_df()
    print("book-related text extracted...")
    original_book = df['text'].iloc[randint(0, df.shape[0]-1)]
    similar_books = []
    # randomly select 10 other books
    for i in range(10):
        similar_books.append(df['text'].iloc[randint(0, df.shape[0]-1)])

    generate_embeddings_and_compute_ranked_distance(original_book, similar_books, 5)

if __name__ == "__main__":
    main()


