from requests import request
from fake_useragent import UserAgent

# for generating fake user agents
user_agents = UserAgent()

# fetches a recipe website by its url and returns its raw text
def fetch_recipe_website(url):
    # create a dict of HTTP request headers (https://developer.mozilla.org/en-US/docs/Glossary/Request_header)
    headers = {
        # we want to spoof a real user agent so the website has a better chance of letting us through
        "User-Agent": user_agents.random
    }
    
    # make the request to the website URL
    response = request("GET", url, headers = headers)

    # get the website content as text from the response
    return response.text


# for local testing
if __name__ == "__main__":
    website_url = input("Enter website URL- ").strip()
    response = fetch_recipe_website(website_url)
    print(response)