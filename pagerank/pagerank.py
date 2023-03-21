import os
import random
import re
import sys

import pandas as pd
import numpy as np
import random
import time


DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)
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
            pages[filename] = set(links)
            # Error with the given code: 
            # pages[filename] = set(links) - {filename}

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
    prop_dist = {}

    # check if page has outgoing links
    dict_len = len(corpus.keys())
    pages_len = len(corpus[page])

    if len(corpus[page]) < 1:
        # no outgoing pages, choosing randomly from all possible pages
        for key in corpus.keys():
            prop_dist[key] = 1 / dict_len

    else:
        # there are outgoing pages, calculating distribution
        random_factor = (1 - damping_factor) / dict_len
        even_factor = damping_factor / pages_len

        for key in corpus.keys():
            if key not in corpus[page]:
                prop_dist[key] = random_factor
            else:
                prop_dist[key] = even_factor + random_factor

    return prop_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Powered by Hu Zhengtao
    
    pr = dict.fromkeys( list( corpus.keys() ) ,0)

    random.seed( time.time())

    N = len( corpus.keys() )
    pl = random.choice(list(corpus.keys())) 
    for i in range(n):
        if random.random() <= damping_factor:

            pl = random.choice(list(corpus[pl]))
            pr[pl] += 1
        else:       
            pl = random.choice(list(corpus.keys()))
            pr[pl] += 1

    for i in pr:
        pr[i] = pr[i] / n
    return pr

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    N = len( corpus )
    pr = dict.fromkeys( list( corpus.keys() ) ,1.0/N)

    flag = True
    while flag:
        p2 = {}
        flag = False
        
        for page in pr.keys():
            p2[page] = (1.0-damping_factor) / N + damping_factor * get_sum(corpus, pr, page)

        for i in pr.keys():
            if abs( pr[i] - p2[i] ) > 0.001:   flag = True
        pr = p2

    return pr


def get_sum(corpus, distribution, page):
    result = 0
    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])
    return result

if __name__ == "__main__":
    main()
