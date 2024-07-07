from urllib import request as req
from base64 import b64encode
import json

def fetch_page(url, page, limit = 70, tags = None, username = None, api = None) -> list:
    url_ = url + f'?tags={tags}&page={page}&limit={limit}'
    request_ = req.Request(url_, headers={
    'User-Agent': 'atimonder1/1.0',
    'Authorization': 'Basic ' + b64encode(f'{username}:{api}'.encode('utf-8')).decode('utf-8')
    }, method='GET')

    with req.urlopen(request_) as res:
        return json.loads(res.read())['posts']

def fetch_all(url, tags = None, username = None, api = None) -> list:
    limit = 20
    post_list = []
    page_counter = 1

    response = ['']
    while response != []:
        response = fetch_page(url, page_counter, limit, tags, username, api)
        
        print(page_counter)
        page_counter += 1

        post_list.append(response)
    return post_list