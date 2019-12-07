**Overview**
The same sample of 2000 books used for word2vec poc is used with a pretrained bert model that has been further trained on NLI datasets to enable textual similarity analsyis from the sentence_transformer library.

In the example file bert_embedding_similarity, no cleaning and tokenization is done as opposed to word2vec since it is handled internally by the library

The main function randomly selects a book from our sample acting as the input for a recommendaiton request, then 10 other books are randomly selected from our dataframe. The bert-nli embeddings are generated for these books and the top 5 are ranked by score and printed to the console.

Our recommendation service will have similar functionality but we will pre-select simlar books based on a combination of user rating and users who shared similar book choices which will refine the base set of books that will be ranked.

Output from script:

book-related text extracted...


Original book: Unmasked: Volume One (Unmasked, #1) I was born int ...

- Top 5 most similar books:
--3D Printing: Rise of the Third Industrial Revoluti ...  (Score: 0.2274)
--Teutonic Knights The Teutonic Knights were powerfu ...  (Score: -0.0225)
--Personal Demon (Women of the Otherworld #8) In her ...  (Score: -0.0318)
--The Hobbit This beautifully presented collector's  ...  (Score: -0.0492)
--The Duke's Husband Jay Wharton and Devon Brooks me ...  (Score: -0.1133)
