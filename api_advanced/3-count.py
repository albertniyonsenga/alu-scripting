#!/usr/bin/python3
"""
3-count
"""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords (case-insensitive).
    """
    if counts is None:
        counts = {}

    # Normalize word_list: count duplicates and lowercase keys
    normalized_words = []
    for w in word_list:
        normalized_words.append(w.lower())
    # Create a dictionary to sum duplicates in word_list
    word_count_map = {}
    for w in normalized_words:
        word_count_map[w] = word_count_map.get(w, 0) + 1

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'linux:count_words:v1.0 (by /u/throwaway)'}
    params = {'limit': 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code != 200:
            # Invalid subreddit or error
            return
        data = response.json()
        posts = data.get("data", {}).get("children", [])
        after = data.get("data", {}).get("after", None)

        for post in posts:
            title = post.get("data", {}).get("title", "").lower()
            # Split title into words by spaces, filter exact matches only
            # We consider a word only if it matches exactly (no punctuation attached)
            # So we split by spaces and check word equality
            title_words = title.split()
            for w in word_count_map:
                # Count occurrences of the exact word in title_words
                # Only count exact matches (case insensitive already handled)
                count = sum(1 for tw in title_words if tw == w)
                if count > 0:
                    counts[w] = counts.get(w, 0) + count

        if after is not None:
            # Recursive call to get next page
            count_words(subreddit, word_list, after=after, counts=counts)
        else:
            # No more pages, print results
            # Multiply counts by the number of duplicates in word_list
            for w in counts:
                counts[w] *= word_count_map[w]

            # Filter out words with zero count
            filtered = {k: v for k, v in counts.items() if v > 0}

            # Sort by count descending, then alphabetically ascending
            sorted_counts = sorted(filtered.items(),
                                   key=lambda x: (-x[1], x[0]))

            for word, count in sorted_counts:
                print(f"{word}: {count}")

    except Exception:
        # On any error, print nothing
        return
