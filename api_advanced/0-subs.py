#!/usr/bin/python3
"""
Reddit Suscriber count module
Working with Reddit API to counts subreddit subscribbers
"""
import requests
import sys

def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers for a given subreddit. 
    Args:
        subreddit(str): Name for the subreddit to query

    Returns:
        int: Number of subcribers(0 for invalid subreddits or errors).
    """
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {'User-Agent': 'Python:RedditAPI.Exercise:v1.0 (by /u/anonymous)'}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.json().get('data', {}).get('subscribers', 0)
        return 0
    except requests.RequestException:
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print(number_of_subscribers(sys.argv[1]))