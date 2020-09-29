import nltk
import sys

FILE_MATCHES = 4
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    import os
    dic = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file), 'r', encoding = 'utf8') as i:
            data = i.read()
            dic[file] = data
    return dic
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    import string
    from nltk.tokenize import word_tokenize
    words_act = []
    words = word_tokenize(document)
    for i in words:
        if i in string.punctuation:
            continue
        elif i in nltk.corpus.stopwords.words('english'):
            continue
        i = i.lower()
        words_act.append(i)
    return words_act
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    def doc_count(word, d):
        count = 0
        for i in d:
            if word in d[i]:
                count += 1
        return count

    import math
    idfs = {}
    total_docs = len(documents)
    for i in documents:
        doc = documents[i]
        for word in doc:
            if word not in idfs:
                docs = doc_count(word,documents)
                idf = math.log(total_docs/docs)
                idfs[word] = idf
    return idfs
    #raise NotImplementedError

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    for i in files:
        score = 0
        for j in query:
            tf = files[i].count(j)
            idf = idfs[j]
            score = score + tf*idf
        scores[score] = i
    li = list(scores.keys())
    li.sort(reverse=True)
    top = []
    for i in range(n):
        top.append(scores[li[i]])
    return top
    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = []
    for i in sentences:
        score = 0
        count = 0
        for j in query:
            if j in sentences[i]:
                score += idfs[j]
                count += 1
        density = count/len(sentences[i])
        scores.append((i,score,density))
    scores.sort(key= lambda x: (x[1],x[2]), reverse = True)
    top = [x[0] for x in scores[:n]]
    return top
    #raise NotImplementedError


if __name__ == "__main__":
    main()
