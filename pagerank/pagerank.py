import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    keys = list(corpus.keys())
    pages = corpus[page]

    probdis = dict()

    for key in keys:
        linked_bonus = 0
        if key in pages:
            linked_bonus = damping_factor/len(pages)
        if len(pages) == 0:
            linked_bonus = damping_factor/len(keys)
        probdis[key] = (1-damping_factor)/len(keys) + linked_bonus

    return probdis
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import random
    import numpy as np
    first = random.choice(list(corpus))
    prob = transition_model(corpus,first, damping_factor)
    summ = {k: 0 for k in set(corpus)}
    summ[first] += 1
    
    if n == 1:
        return prob
    
    for i in range(n-1):
        """
        total = 0
        rand = random.random()
        nex = ''
        for key,value in prob.items():
            total += value
            if rand <= total:
                nex = key
                break """
        nex = np.random.choice(list(prob.keys()), 1, replace = True, p = list(prob.values()))[0]
        temp = transition_model(corpus, nex, damping_factor)
        summ[nex] += 1
        prob = temp
    summ = {k: summ.get(k,0)/n for k in set(summ)}
    return summ
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    import copy
    dic = {k: 1/len(corpus) for k in set(corpus)}
    diff = copy.deepcopy(dic)
    flag = 1
    
    while flag == 1:
        for key in dic:
            summ = (1-damping_factor)/len(corpus)
            for i in corpus:
                if key in corpus[i]:
                    summ = summ + damping_factor*(dic[i]/len(corpus[i]))
                else:
                    continue
            diff[key] = abs(dic[key] - summ)
            dic[key] = summ
            
        for i in diff:
            if diff[i] >= 0.001:
                flag = 1
                break
            else:
                flag = 0
               
    return dic

#raise NotImplementedError


if __name__ == "__main__":
    main()
