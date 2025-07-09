#!/usr/bin/python3
"""
Recursive function to query Reddit API, parse titles of hot articles,
and print a sorted count of given keywords (case-insensitive).
"""

import argparse
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}

    word_counts = {}
    for w in word_list:
        lw = w.lower()
        word_counts[lw] = word_counts.get(lw, 0) + 1

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'linux:count_words:v1.0 (by /u/throwaway)'}
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            if counts:
                _print_counts(counts, word_counts)
            return

        data = response.json()
        posts = data.get('data', {}).get('children', [])
        if not posts and not counts:
            return

        for post in posts:
            title = post['data']['title'].lower().split()
            words_in_title = [w.strip('.,!?:;"\'()[]{}') for w in title]
            for w in word_counts.keys():
                counts[w] = counts.get(w, 0) + words_in_title.count(w)

        after = data.get('data', {}).get('after', None)
        if after is None:
            _print_counts(counts, word_counts)
            return

        return count_words(subreddit, word_list, after, counts)

    except Exception:
        if counts:
            _print_counts(counts, word_counts)
        return


def _print_counts(counts, word_counts):
    final_counts = {}
    for word, dup_count in word_counts.items():
        if word in counts and counts[word] > 0:
            final_counts[word] = counts[word] * dup_count

    if not final_counts:
        return

    sorted_counts = sorted(final_counts.items(),
                           key=lambda x: (-x[1], x[0]))

    for word, count in sorted_counts:
        print(f"{word}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count occurrences of keywords in hot posts of a subreddit."
    )
    parser.add_argument("subreddit", type=str, help="Name of the subreddit")
    parser.add_argument("keywords", type=str,
                        help="Space-separated list of keywords to count (put in quotes)")
    args = parser.parse_args()

    keywords_list = args.keywords.split()
    counts = count_words(args.subreddit, keywords_list)

    if counts:
        # Prepare word_counts dictionary for duplicates count
        word_counts = {}
        for w in keywords_list:
            lw = w.lower()
            word_counts[lw] = word_counts.get(lw, 0) + 1

        _print_counts(counts, word_counts)

