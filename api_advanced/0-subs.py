#!/usr/bin/python3
"""Retrieve the number of subscribers for a given subreddit.

Args:
    subreddit (str): The name of the subreddit to query

Returns:
    int: Number of subscribers if subreddit is valid, 0 otherwise
"""
import requests
import sys

def number_of_subscribers(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "linux:subreddit.subs:v1.0 (by /u/throwaway)"}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.json().get("data", {}).get("subscribers", 0)
        return 0
    except requests.RequestException:
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print(number_of_subscribers(sys.argv[1]))