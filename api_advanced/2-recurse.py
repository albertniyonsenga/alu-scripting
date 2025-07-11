#!/usr/bin/python3
"""Recursively retrieve titles of all hot articles for a given subreddit.

Args:
    subreddit (str): The subreddit to query.
    hot_list (list): Accumulator list of titles (used in recursion).
    after (str): The 'after' parameter for pagination (used in recursion).

Returns:
    list: List of titles of all hot posts if subreddit is valid.
    None: If subreddit is invalid or no results found.
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'linux:recurse:v1.0 (by /u/throwaway)'}
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            if not posts and not hot_list:
                # No posts found on first call means invalid or empty subreddit
                return None

            for post in posts:
                hot_list.append(post['data']['title'])

            after = data.get('data', {}).get('after', None)
            if after is None:
                return hot_list  # No more pages, return accumulated list

            # Recursive call to get next page
            return recurse(subreddit, hot_list, after)

        else:
            # Status code not 200 means invalid subreddit or error
            return None

    except Exception:
        return None
    
