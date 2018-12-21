import sys, os
import re
import requests
import unirest
import HTMLParser

"""
NOTE:
Before running this script, make sure to set your API-KEY(s) to environment variables
$ export API_KEY_X_MASHAPE=YOUR-API-KEY
$ export API_KEY_BING=YOUR-API-KEY
"""

## #text normalization
html_parser = HTMLParser.HTMLParser()
def remove_u(word):
    word_u = (word.encode('unicode-escape')).decode("utf-8", "strict")
    if r'\u' in word_u: 
        return " ".join(word_u.split('\\u'))
    return word

def normalize(text):
    text = html_parser.unescape(" ".join(re.sub( r'<[^>]*>', ' ', text).split()))
    return " ".join([remove_u(token) for token in text.split()])


# a search API for free (https://rapidapi.com/contextualwebsearch/api/web-search)
class ContextualWebSearchAPI:
    def __init__(self, apikey):
        self.apikey = apikey
        self.html_parser = HTMLParser.HTMLParser()

    def get_snippets(self, query, num_snippets=100, autoCorrect=True):
        query = "%20".join(query.split())
        pages = num_snippets//50 + 1
        snippets = []

        for p in range(pages):
            response = requests.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPIWithPagination?autoCorrect={}&pageNumber={}&pageSize=50&q={}&safeSearch=true".format(autoCorrect, str(p+1), query),
            headers={"X-RapidAPI-Key": self.apikey, "Accept": "application/json"}).json()

            for webPage in response["value"]:
                description = webPage["description"]
                snippets.append(normalize(description))
        return snippets[:num_snippets]


# Bing Search (if you have an account for bing search API)
# (https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-web-api-v7-reference)
class BingSearchApi:
    def __init__(self, apikey):
        self.bing_subscription_key = apikey
        self.search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
        self.html_parser = HTMLParser.HTMLParser()
    
    def remove_u(self, word):
        word_u = (word.encode('unicode-escape')).decode("utf-8", "strict")
        if r'\u' in word_u: 
            return " ".join(word_u.split('\\u'))
        return word

    def normalize(self, text):
        text = self.html_parser.unescape(" ".join(re.sub( r'<[^>]*>', ' ', text).split()))
        return " ".join([self.remove_u(token) for token in text.split()])

    def get_snippets(self, query, num_snippets=100):
        snippets = []
        for offset in range(0, num_snippets, 50): # we get up to 100 results
            headers = {"Ocp-Apim-Subscription-Key" : self.bing_subscription_key}
            params  = {"q": query, "textDecorations":True, "textFormat":"HTML", "count": 50}
            response = requests.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()

            search_results = response_json["webPages"]['value']
            for result in search_results:
                snippets.append(self.normalize(result['snippet']))

        #return snippets
        return snippets[:num_snippets]


if __name__ == "__main__":
    # unittest

    """
    query = "Donald NOT Trump"
    bing_subscription_key = os.environ["API_KEY_BING"]
    bing_search = BingSearchApi(bing_subscription_key)
    snippets = bing_search.get_snippets(query, num_snippets=100)
    print(snippets)
    print(len(snippets))
    """
    query = "Donald -Trump"
    X_Mashape_Key = os.environ["API_KEY_X_MASHAPE"]
    contextual_web_search = ContextualWebSearchAPI(X_Mashape_Key)
    snippets = contextual_web_search.get_snippets(query, num_snippets=100)
    print(snippets)
    print(len(snippets))
