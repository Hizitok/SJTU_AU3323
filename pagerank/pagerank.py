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
    ####################
    ## YOUR CODE HERE ##
    ####################

    # Powered by Hu Zhengtao
    
    pr = dict.fromkeys( list( corpus.keys() ) ,0)

    random.seed( time.time())
    num = 0
    pages = {}
    for i in corpus.keys():
        pages[num] = i
        num = num + 1
    def rd_page():        
        rd = random.randint(0,num-1)
        return pages[ rd ]    

    pl = rd_page()
    for i in range(n):
        rdm = random.random()
        if rdm <= damping_factor:
            while ( a := rd_page() )  not in corpus[pl]:
                pass
            pr[pl := a] += 1

            # With Low Efficiency!!! 
            # Every random element of set cost much
        else:       
            pl = rd_page()
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
    ####################
    ## YOUR CODE HERE ##
    ####################

    N = len( corpus )
    pr = dict.fromkeys( list( corpus.keys() ) ,1/N)

    linkin = {}
    for i in corpus.keys():
        for j in corpus[i]:
            if j not in linkin.keys():
                linkin[j] = []
            linkin[j].append(i)

    flag = True
    while flag:
        p2 = {}
        for i in pr.keys():
            p2[i] = (1-damping_factor) / N + damping_factor * sum(  pr[j] / len( corpus[j] ) for j in linkin[i] ) 

        flag = False
        for i in pr.keys():
            if abs( pr[i] - p2[i] ) > 0.001:   flag = True
        pr = p2
    return pr


if __name__ == "__main__":
    main()
