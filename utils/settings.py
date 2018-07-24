from user_agent import generate_user_agent

# Headers that will be used for the requests.

HEADERS_DEFAULT = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": generate_user_agent(),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

# Default proxies list that we have in the project.

PROXIES_LIST = []
