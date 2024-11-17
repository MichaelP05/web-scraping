import requests
import hashlib
import re

def make_joblist(content):
    job_titles = re.findall(r'<div class="job_secteur_title"[^>]*>(.*?)<\/div>', content)  # Замініть <div> на потрібний тег
    #job_titles = re.findall(r'<div[^>]*class="[^"]*job_selecture_title[^"]*"[^>]*>(.*?)</div>', content)  
    
    # Очищення результату від зайвих пробілів та HTML-тегів
    job_titles = [re.sub(r'<[^>]+>', '', title).strip() for title in job_titles]
    return job_titles

def make_joblist_with_url(url, content):

    titles_pattern = r'<div class="job_secteur_title"[^>]*>(.*?)</div>'
    titles = re.findall(titles_pattern, content)
    
    # Регулярний вираз для пошуку URL вакансій
    links_pattern = r'<a href="https:\/\/www.lejobadequat.com\/emplois\/([^"]+)"'
    links = re.findall(links_pattern, content)
    
    # Формування списку вакансій
    jobs = [
            {"title": re.sub(r'<[^>]+>', '', title).strip(), "url": f"{url}/{link}"}
            for title, link in zip(titles, links)
        ]
    return jobs
    

def get_content(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r') as f:
            content = f.read()
            #print(content)
            return content
    except:
        response = requests.get(url)
        print('Request was sent')
        with open(name, 'w') as f:
            f.write(response.text)
        return response.text

def post_content(url, preload=''):
    response = requests.post(url, preload)
    print(response.text)


if __name__ == '__main__':
    
    url = 'https://www.lejobadequat.com/emplois'
    preload = ''
    print(make_joblist(get_content(url)))
    print('================================================================')
    print(make_joblist_with_url(url, get_content(url)))

