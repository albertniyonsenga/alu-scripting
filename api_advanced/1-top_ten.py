#!/usr/bin/python3
import requests
import argparse

def top_ten(subreddit):
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
