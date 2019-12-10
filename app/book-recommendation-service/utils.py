import ast


def extract_list_from_string(text):
    if isinstance(text, list):
        return text
    else:
        return ast.literal_eval(text)


def convert_book_ids_to_goodreads_id(book_list, book_id_map):
    converted_list = []
    for book in book_list:
        if book in book_id_map:
            converted_list.append(book_id_map[book])
    return converted_list
