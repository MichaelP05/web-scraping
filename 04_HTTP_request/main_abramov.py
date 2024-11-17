import requests
import re
import hashlib


def get_request():
    url = 'https://www.lejobadequat.com/emplois'
    response = requests.get(url)
    print(response.status_code)
    print(response.text)


def post_request():
    url = 'https://www.lejobadequat.com/emplois'
    payload = {
        "action": "facetwp_refresh",
        "data": {
            "facets": {
                "recherche": [],
                "ou": [],
                "type_de_contrat": [],
                "fonction": [],
                "load_more": [
                    3
                ]
            },
            "frozen_facets": {
                "ou": "hard"
            },
            "http_params": {
                "get": [],
                "uri": "emplois",
                "url_vars": []
            },
            "template": "wp",
            "extras": {
                "counts": True,
                "sort": "default"
            },
            "soft_refresh": 1,
            "is_bfcache": 1,
            "first_load": 0,
            "paged": 3
        }
    }
    response = requests.post(url, json=payload)
    print(response.status_code)
    print(response.text)


def use_header():
    url = 'https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/'
    response = requests.get(url)
    print(response.status_code)
    print(response.text)

    pattern = '<th>USER-AGENT<\/th>\s*<td>(.+?)<\/td>'
    user_agent = re.search(pattern, response.text).group(1)
    print(user_agent)

    fake_header_response = requests.get(
        url,
        headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
    )
    user_agent = re.search(pattern, fake_header_response.text).group(1)
    print(user_agent)


def get_content(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r') as f:
            content = f.read()
            return content
    except:
        response = requests.get(url)
        print('request was sent')
        with open(name, 'w') as f:
            f.write(response.text)
        return response.text


if __name__ == '__main__':
    # get_request()
    # post_request()
    # use_header()
    text = get_content('https://www.lejobadequat.com/emplois')
    print(text[:10])
    text = get_content('https://jobs.marksandspencer.com/job-search?country%5B0%5D=United%20Kingdom&page=3&radius=')
    print(text[:10])
    text = get_content('https://www.lejobadequat.com/emplois')
    print(text[:10])
