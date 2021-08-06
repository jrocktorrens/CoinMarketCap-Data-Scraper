import requests
import logging


def search_google(query, api_key, search_engine_id):
    page = 1
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&start={start}"
    data = requests.get(url).json()
    error = data['error']
    if error['code'] != 429:
        search_items = data['items']
        search_info = data['searchInformation']
        total_results = search_info['totalResults']
        web_sites = ''
        for i, search_item in enumerate(search_items):
            web_sites += search_item['link'] + '\n'
        logging.info('Google api succeeded reading info from google!')
        return total_results, web_sites
    else:
        logging.error('Google api Error! Limit of searches exceeded.')
        return None, None
