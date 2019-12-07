To complete the POC, used a sample of around 2,000 books from the goodreads_books.json dataset

**Text Extraction + Cleaning**
filename: extract_clean_calculate_similarity.py
Extracted the book_id, title, description, and popular shelves with more than 50 uses.
The book_id will be needed to integrate with other pieces of the recommendation system
and the text fields will be used in aggregate to rank similarity based on sentence embeddings.
Currently stored this information in a dataframe with 2 columns - book_id and text - ideally this
should be precomputed for all our book data for quick lookup.

Next the text was cleaned/normalized using these methods:
- remove punctuation
- remove stopwords
- tokenized
- stemming

**Similarity Calculation**
Used the word2vec google news model to compute similarity between two book texts.

In current code, two books are randomly chosen from the dataframe - the text object is printed
out before calculating the distance

Note: word2vec seems quite slow as it's doing a vector similarity computation across the corpus.
Did some research on fastText which seems to be faster (no surprise there!)

**Next steps**
- Look into other ready models that we can use
- See if training a custom NN or using transfer learning will give us better results
- Maybe labels can be derived from existing similar books data
- Once we are satisfied with book text extraction - precompute this for full corpus

Sample run output:

```
extracted...
cleaning starts now...
punctuation removed...
tokenized...
removed stop words...
stemmed...
cleaning is complete
love mean patienc love mean stori year discharg marin dont ask dont tell codi culver live ptsdinduc world mission misconcept geoff eli enemi codi break farmhous quickli brought back sens fri pan head receiv much need help hospit codi nowher go luckili kindheart eli know turn eli ask former marin brick hunter help brick isnt sure want get involv brick work ptsd like owe eli favor codi struggl rejoin real world brick agre take discov common either thought possibl though codi tri stay sometim flash unexplain traumat eventsev dont fit usual war zone delus delus grow frequent becom appar might delus codi may actual wit murder
earth move one minut your work make horoscop local paper next your team sexi secret agent call charli tri help solv case celebr crime investig agenc amber make horoscop local paper wish excit life get phone call offer call heartthrob actor enni mckarthi old uni boyfriend beg favour brother joel found dead suspici circumst desper keep stori newspap solv mysteri brother death fast possibl enni call specialist shape ccia celebr crime investig agenc man job top agent charli huxton enni stalk journalist paparazzi doesnt trust stranger handl case keep quiet might discov plead amber want shadow charli throughout investig much amber surpris charli eventu agre leav wonder what charli amber delv joel death soon hand full question potenti suspect victim irat exgirlfriend discov theyr battl someth far danger could ever expectedand grow attract mayb amber life get excit
Similarity score: 0.32
```


