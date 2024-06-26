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

    RETURN: dictionary with probability distribution of which page is going to be visited next
    """
    output = dict()

    # calculate probability of redirected pages
    for link in corpus[page]:
        p = damping_factor / len(corpus[page])
        output[link] = p

    # calculate the probability of a random page
    for link in corpus:
        p = (1 - damping_factor) / len(corpus)
        if link in output:
            output[link] += p
        else:
            output[link] = p

    return output

def sample_pagerank(corpus, damping_factor, page, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # make dict to collect page occurences
    output = dict()
    for link in corpus:
        output[link] = 0

    # pick random page from corpus
    page = random.choice(list(corpus.keys()))
    output[page] += 1

    # iterate over remaining sample (-1)
    for i in range(n - 1):
        p_dis = transition_model(corpus, page, damping_factor)
        next = random.choices(
            population=list(p_dis.key()), weights=list(p_dis.values())
        )[0]
        output[next] += 1
        page = next
    
    # calculate page rank
    for page in output:
        output[page] = output[page] / n

    return output

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
  # modify corpus to account for pages without redirect links
    for page, links in corpus.items():
        if not links:
            corpus[page] = list(corpus.keys())
    
    # assign equal probability to each page in initial step
    if not probability_distribution:
        probability_distribution = dict()
        for link in corpus:
            probability_distribution[link] = 1 / len(corpus)
    # get new page rank
    new_probability_distribution = dict()
    for link in corpus:
        p = (1 - damping_factor) / len(corpus) # first part of iterative formul
        p += agg_source_pagerank(page=link, probability_distribution=probability_distribution,corpus=corpus, damping_factor=damping_factor)
        new_probability_distribution[link] = p

    # check for difference between old and new (< 0.001)
    diff_list = []
    for page in new_probability_distribution:
        diff_list.append(abs(new_probability_distribution[page] - probability_distribution[page]))

    if max(diff_list) > 0.001:
         # check if difference is still too high
        return iterate_pagerank(
            corpus=corpus,
            damping_factor=damping_factor,
            probability_distribution=new_probability_distribution,
        )
    else:
        return new_probability_distribution
    
def agg_source_pagerank(page, probability_distribution, corpus, damping_factor):
    """
    Helper method to calculate the second part of the iterative method.
    """
    p = 0
    source_pages = []
    # get source pages
    for link in corpus:
        if page in corpus[link]:# and page not in source_pages:
            source_pages.append(link)
    # calculate probability of being on source page
    for source in source_pages:
        number_links = len(corpus[source])
        p += damping_factor * (probability_distribution[source] / number_links)

    return p


if __name__ == "__main__":
    main()
