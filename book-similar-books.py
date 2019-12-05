import json
import csv
import pandas as pd
import random

# goodreads_books_path = 'data/goodreads_books.json'
goodreads_interactions_path = 'data/goodreads_interactions.csv'
save_file_name = "results/book_to_similar_books.csv"
test_mode = False
random.seed(10)

user_to_book_dict = {}
book_to_user_dict = {}
with open(goodreads_interactions_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    count = 0
    for line in csv_reader:
        #         print(line)
        rating = line[3]
        if rating != "4" and rating != "5":
            continue
        user_id = line[0]
        book_id = line[1]

        # build the user_to_book_dict
        if user_id in user_to_book_dict:
            user_to_book_dict[user_id].append(book_id)
        else:
            user_to_book_dict[user_id] = [book_id]

        # build the book_to_user_dict
        if book_id in book_to_user_dict:
            book_to_user_dict[book_id].append(user_id)
        else:
            book_to_user_dict[book_id] = [user_id]

        # test
        if test_mode:
            count += 1
            if count == 10:
                break


# print book_to_user_dict
print('Here ---- 1')
for item in list(book_to_user_dict.items())[:1]:
    print('book_to_user_dict item: ', item)
    print()

# print user_to_book_dict
print('Here ---- 2')
for item in list(user_to_book_dict.items())[:1]:
    print('user_to_book_dict item: ', item)
    print()


# build the book_to_similar_books_dict
book_to_similar_books_dict = {}
for book_id, user_id_list in book_to_user_dict.items():
    book_to_similar_books_dict[book_id] = []
    if len(user_id_list) > 50:
        user_id_list_slice = random.sample(user_id_list, 50)
    else:
        user_id_list_slice = user_id_list
    for user_id in user_id_list_slice:
        user_books_list = user_to_book_dict[user_id]
        if len(user_books_list) > 4:
            user_books_slice = random.sample(user_books_list, 4)
        else:
            user_books_slice = user_books_list
        book_to_similar_books_dict[book_id].extend(user_books_slice)
    # write to csv


# print user_to_book_dict
print('Here ---- 3')
for item in list(book_to_similar_books_dict.items())[:1]:
    print('book_to_similar_books_dict item: ', item)
    print()

# Dataframe ----
df_book_to_similar_books = pd.DataFrame([(i,','.join(j)) for i, j in book_to_similar_books_dict.items()], columns=['book_id', 'similar_books_id'])
df_book_to_similar_books = df_book_to_similar_books.drop(0) # remove unnecessary column name
# df_book_to_similar_books.head()

# write to csv
print('---- About to write to disk')
df_book_to_similar_books.to_csv(save_file_name, index=False)






