import sys, os
import re
import requests
import unirest
import HTMLParser
import pprint
from googleapiclient.discovery import build

"""
NOTE:
Before running this script, make sure to set your API-KEY(s) to environment variables
$ For CWS api
$ export API_KEY_X_MASHAPE=YOUR-API-KEY

$ For Bing api
$ export API_KEY_BING=YOUR-API-KEY

$ For Google search api
$ export GOOGLE_DEVELOPER_KEY=YOUR-GDK_KEY (at https://console.cloud.google.com/apis/credentials)
$ export GOOGLE_CSE_KEY=YOUR_CSE_KEY (at  https://cse.google.com/cse/all)
 
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
            try:
                response = requests.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPIWithPagination?autoCorrect={}&pageNumber={}&pageSize=50&q={}&safeSearch=false".format(autoCorrect, str(p+1), query),
                headers={"X-RapidAPI-Key": self.apikey, "Accept": "application/json"}).json()

                for webPage in response["value"]:
                    description = webPage["description"]
                    snippets.append(normalize(description))

            # This API is not stable. Ignore the API errors (RuntimeError, simplejson.errors.JSONDecodeError, etc.)
            except:
                pass

        #assert len(snippets) > 0 # warning?
        if len(snippets) == 0:
            return []
        else:
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
        for offset in range(0, num_snippets, 50):
            headers = {"Ocp-Apim-Subscription-Key" : self.bing_subscription_key}
            params  = {"q": query, "textDecorations":True, "textFormat":"HTML", "count": 50}
            response = requests.get(self.search_url, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()

            try:
                search_results = response_json["webPages"]['value']
                for result in search_results:
                    snippets.append(self.normalize(result['snippet']))
            except KeyError:
                pass

        #return snippets
        return snippets[:num_snippets]


# Google Search
class GoogleSearchApi:
    
    def __init__(self, apikey, csekey):
        self.developerKey = apikey
        self.service = build("customsearch", "v1", developerKey=self.developerKey)
        self.html_parser = HTMLParser.HTMLParser()
        self.GOOGLE_CSE_KEY=csekey

    def remove_u(self, word):
        word_u = (word.encode('unicode-escape')).decode("utf-8", "strict")
        if r'\u' in word_u: 
            return " ".join(word_u.split('\\u'))
        return word

    def normalize(self, text):
        text = self.html_parser.unescape(" ".join(re.sub( r'<[^>]*>', ' ', text).split()))
        return " ".join([self.remove_u(token) for token in text.split()])


    def get_snippets(self, query, query_exclude=None):
        snippets = []
        response_json = self.service.cse().list(q=query, cx=self.GOOGLE_CSE_KEY, excludeTerms=query_exclude).execute()
        if "items" in response_json.keys():
            for res in response_json["items"]:
                snippets.append(self.normalize(res["htmlSnippet"]))
        return snippets


if __name__ == "__main__":

    # Google
    query = "Donald"
    query_ex = "Trump"
    google_developer_key = os.environ["GOOGLE_DEVELOPER_KEY"]
    google_cse_key = os.environ["GOOGLE_CSE_KEY"]
    google_search = GoogleSearchApi(google_developer_key, google_cse_key)
    snippets = google_search.get_snippets(query, query_exclude=query_ex)
    print(snippets)

    # Bing
    #query = "Donald NOT Trump"
    bing_subscription_key = os.environ["API_KEY_BING"]
    bing_search = BingSearchApi(bing_subscription_key)
    snippets = bing_search.get_snippets(query, num_snippets=10)
    print(snippets)
    print(len(snippets))

    # cws
    query = "Donald -Trump"
    X_Mashape_Key = os.environ["API_KEY_X_MASHAPE"]
    contextual_web_search = ContextualWebSearchAPI(X_Mashape_Key)
    snippets = contextual_web_search.get_snippets(query, num_snippets=10, autoCorrect=False)
    print(snippets)
    print(len(snippets))
