import requests

API_KEY = 'AIzaSyDmHyS90a7rj6nwXMsQeO9-5id9pSjHHOI'
SEARCH_ENGINE_ID = 'f6368e2e556c1f9c9'


def search_google(query, api_key, search_engine_id):
    page = 1
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
    data = requests.get(url).json()
    search_items = data['items']
    search_info = data['searchInformation']
    total_results = search_info['totalResults']
    web_sites = []
    for i, search_item in enumerate(search_items):
        web_sites.append(search_item['link'])

    return total_results, web_sites

