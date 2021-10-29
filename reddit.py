#!/usr/bin/env python3

import argparse  # for parsing arguments
import json  # for formatting and printing json
import requests  # for making HTTP requests


def build_parser():
    """
    Builds an ArgumentParser with the specified parameters.

    Args:
        None

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Pulls top posts from subreddit and displays them in terminal")
    parser.add_argument('url', help="the URL or subreddit to visit")
    parser.add_argument('-n', type=int, default=10, help="number of posts to display (default: 10)")
    parser.add_argument('-o', type=str, default="score", help="field to sort posts by (default: score)")
    parser.add_argument('-t', type=int, default=60, help="truncate title to specified length (default: 60)")
    return parser


def load_reddit_data(url):
    """

    Args:
        url (str): the url (or subreddit)

    Returns:
        list: a list of dicts containing post information for the subreddit.
    """
    i = 0
    http = "http"
    url_concat = url[:4]
    if http != url[:4]:
        url = "https://www.reddit.com/r/" + url + "/.json"
    headers = {"user-agent": "Reddit_script by amlaban@sas.upenn.edu"}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json['data']['children']


def format_reddit_data(data, limit=10, order_by="score", title_len=60):
    """

    Args:
        data (list): a list of dicts containing the raw reddit post data from
            load_reddit_data
        limit (int): the number of posts to return, default 10
        order_by (str): the attribute in the raw reddit post data to sort by,
            default "score"
        title_len (int): the length of the title to show, default 60

    Returns:
        list: a list of dicts with with the following attributes in each dict:
            title (str): the possibly shortened post title
            score (str): the score of the post
            url (str): the url to the post
    """
    formatted_list = []
    for i in range(limit):
        d = {}
        title = data[i]['data']['title']
        title_concat = title[:title_len]
        d['title'] = title_concat
        d['score'] = data[i]['data']['score']
        d['url'] = data[i]['data']['url']
        formatted_list.append(d)
    if order_by == "score":
        formatted_list.sort(key=lambda d: d['score'], reverse=True)
    else:
        formatted_list.sort(key=lambda d: d['score'])
    return formatted_list


def print_reddit_data(formatted_data):
    """
    Args:
        formatted_data (list): a formatted list of posts returned from
            format_reddit_data()

    Returns:
        None
    """
    for i in range(len(formatted_data)):
        print("{index}.\t{title} (Score: {score})\n\t{url}".format(index=i,
            title=formatted_data[i]['title'], score=formatted_data[i]['score'],
                url=formatted_data[i]['url']))


def main():
    """
    Builds an ArgumentParser object by calling build_parser(),
    loads the data from the given URL by calling load_reddit_data(),
    and then prints the data using print_reddit_data().
    """
    parser = build_parser()
    # Parse command line arguments
    args = parser.parse_args()

    url = args.url
    limit     = args.n
    orderby   = args.o
    titlelen  = args.t

    # Load data from url and then print the data
    data = load_reddit_data(url)
    formatted_data = format_reddit_data(data, limit, orderby, titlelen)
    print_reddit_data(formatted_data)


if __name__ == '__main__':
    main()
