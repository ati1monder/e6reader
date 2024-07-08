from urllib import request as req
from base64 import b64encode
import json

def fetch_page(url, page, limit = 70, tags = None, username = None, api = None) -> list:
    print("Fetching API posts...")
    url_ = url + f'?tags={tags}&page={page}&limit={limit}'
    request_ = req.Request(url_, headers={
    'User-Agent': 'atimonder1/1.0',
    'Authorization': 'Basic ' + b64encode(f'{username}:{api}'.encode('utf-8')).decode('utf-8')
    }, method='GET')

    with req.urlopen(request_) as res:
        print('Loaded successfully!')
        return json.loads(res.read())['posts']

def fetch_all(url, tags = None, username = None, api = None, limit = 70) -> list:
    limit_full = 370
    post_list_full_limit = []
    page_counter = 1

    response = ['']
    while True:
        response = fetch_page(url, page_counter, limit_full, tags, username, api)

        if not response:
            break
        
        print(page_counter)
        page_counter += 1

        post_list_full_limit.append(response)
    
    response_ = []
    for item in post_list_full_limit:
        for x in item:
            response_.append(x)

    post_list_sorted = []
    item_count = 0
    for i in range(len(response_) // limit):
        post_list_sorted.append([])
        for j in range(limit):
            post_list_sorted[i].append(response_[item_count])
            item_count += 1
    if item_count < len(response_):
        post_list_sorted.append([])
        while item_count < len(response_):
            post_list_sorted[-1].append(response_[item_count])
            item_count += 1
    
    return post_list_sorted