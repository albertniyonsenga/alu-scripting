#!/usr/bin/python3
"""
Reddit API Hot Posts Module

This module provides functionality to query the Reddit API
and retrieve the titles of hot posts for a given subreddit.
The script handles both existing and non-existent subreddits
and can be run from the command line with a subreddit argument.
"""

import argparse
import requests


def top_ten(subreddit):
    """
    Retrieve and print the titles of the first 10 hot posts from a specified subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to query.
    
    Returns:
        None: Function prints the titles directly or prints None for invalid subreddits.
    """
    # Rest of your function code...

    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
    headers = {
        'User-Agent': 'linux:top_ten:v1.0 (by /u/throwaway)',
        'Accept': 'application/json'
        }
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        print("Status Code:", response.status_code)
        print("Response:", response.text)

        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            for post in posts:
                print(post['data']['title'])
        else:
            print(None)
    except requests.RequestException:
        print(None)
    except (KeyError, ValueError):
        print(None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get top 10 hot posts from a subreddit.")
    parser.add_argument("subreddit", type=str, help="Name of the subreddit")
    args = parser.parse_args()
    top_ten(args.subreddit)
