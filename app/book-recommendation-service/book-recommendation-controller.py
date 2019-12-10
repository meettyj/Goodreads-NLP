import warnings

from flask import Flask
from flask import request
import json
import load_data_initialize_model as preloaded
import scipy

app = Flask(__name__)

warnings.filterwarnings("ignore")


def retrieve_similar_books(book_id):
    if book_id in preloaded.similar_books_map:
        return list(preloaded.similar_books_map[book_id])
    return []


def retrieve_book_descriptions(book_ids):
    similar_book_descriptions = {}
    for item in book_ids:
        if item in preloaded.book_id_descriptions:
            similar_book_descriptions[item] = preloaded.book_id_descriptions[item]
    return similar_book_descriptions


def rank_recommendations_based_on_similarity(original, similar_book_texts, n):
    response_object = []
    original_text = original[1]
    similar_book_ids = list(similar_book_texts.keys())
    similar_texts = list(similar_book_texts.values())
    orig_book_embedding = preloaded.model.encode(original_text, bsize=128, tokenize=False)[0]
    similar_books_embeddings = preloaded.model.encode(similar_texts, tokenize=True, verbose=True)
    distances = scipy.spatial.distance.cdist([orig_book_embedding], similar_books_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    for idx, distance in results[0:n]:
        print(similar_texts[idx].strip()[0:50], "... ",  "(Score: %.4f)" % (1 - distance))
        book_recommendation = {}
        book_id = similar_book_ids[idx]
        book_recommendation['book_id'] = book_id
        book_title = "Unknown"
        if book_id in preloaded.book_id_titles:
            book_title = preloaded.book_id_titles[book_id]
        book_recommendation['book_title'] = book_title
        book_recommendation['book_description'] = preloaded.book_id_descriptions[book_id]
        response_object.append(book_recommendation)
    return response_object


def construct_request_summary_object(book_id):
    response = {}
    book_title = 'Unknown'
    book_desc = 'N/A'
    if book_id in preloaded.book_id_titles:
        book_title = preloaded.book_id_titles[book_id]
    response['book_title'] = book_title
    if book_id in preloaded.book_id_descriptions:
        book_desc = preloaded.book_id_descriptions[book_id]
    response['book_description'] = book_desc
    return response


@app.route('/book-recommendations', methods=['GET'])
def recommend_books():
    data = {}
    status = 200
    message = 'Successful'
    response_object = []
    requested_book_id = request.args.get('book_id')
    top_n = int(request.args.get('top_n'))

    # don't return more than 15 results
    if top_n > 15 or top_n is None:
        top_n = 15
    similar_books = retrieve_similar_books(requested_book_id)
    if len(similar_books) > 0 and requested_book_id in preloaded.book_id_descriptions:
        requested_book_desc = preloaded.book_id_descriptions[requested_book_id]
        book_descriptions = retrieve_book_descriptions(similar_books)
        response_object = rank_recommendations_based_on_similarity([requested_book_id, requested_book_desc],
                                                                       book_descriptions, top_n)
    else:
        status = 201
        message = 'No recommendations found for book_id: ' + requested_book_id

    data['status'] = status
    data['message'] = message
    data['requestSummary'] = construct_request_summary_object(requested_book_id)
    data['recommendations'] = response_object
    json_data = json.dumps(data)
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0')
