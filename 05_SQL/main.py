import requests
import hashlib
import re
import csv, json, sqlite3
import os

def make_joblist(content:list):
    job_titles = re.findall(r'<div class="job_secteur_title"[^>]*>(.*?)<\/div>', content)  # Замініть <div> на потрібний тег
    
    # Очищення результату від зайвих пробілів та HTML-тегів
    job_titles = [re.sub(r'<[^>]+>', '', title).strip() for title in job_titles]
    return job_titles

def make_joblist_with_url(url:str, content:list) -> list:

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
    
    name = os.path.join(os.getcwd(), hashlib.md5(url.encode('utf-8')).hexdigest())
    try:
        with open(name, 'r') as f:
            content = f.read()
            return content
    except:
        response = requests.get(url)
        print(f'Запит відправлено. Response status code: {response.status_code}')
        with open(name, 'w') as f:
            f.write(response.text)
        print(response.status_code)
        return response.text

def into_csv(data: list) -> None:
    filename = 'result.csv'
    try: 
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'url'])
            writer.writerows([[item["title"], item["url"]] for item in data])
    except Exception as e:
        print(f"Помилка при записі в CSV: {e}")

def into_json(data: list) -> None:
    filename = 'result.json'
    
    try:
        with open(filename, mode='w') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"Помилка при записі в JSON: {e}")

def write_into_sql(fn, data: list) -> None:
    
    # 1. create table
    conn = sqlite3.connect(os.path.join(os.getcwd(), fn))
    cursor = conn.cursor()

    sql = """
        create table if not exists job_list (
            id integer not null primary key,
            title text,
            url text,
            is_read boolean default false
        )
    """
    cursor.execute(sql)

    # 2. insert data
    
    for item in data:
        print(item["title"],item["url"])
        cursor.execute("""
            insert into job_list (title, url)
            values (?, ?)
        """, (item["title"], item["url"]))

    conn.commit()
    conn.close()


def read_from_sql(fn) -> None:
    
    conn = sqlite3.connect(os.path.join(os.getcwd(), fn))
    cursor = conn.cursor()

    # 1. get all of job_list
    sql = """
        select * from job_list
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)
    print("="*60)
    
    # 2. get title from job_list where is_read=false
    sql = """
        select title
        from job_list
        where is_read = false
    """
    rows = cursor.execute(sql).fetchall()
    print(rows)
    print("="*60)
    conn.close()
    

def up_to_date_sql(fn, data: list) -> None:
    
    conn = sqlite3.connect(os.path.join(os.getcwd(), fn))
    cursor = conn.cursor()

    # 1. update data
    for item in data:
        cursor.execute("""
            UPDATE job_list
            SET title = ?, url = ?, is_read = ?
            WHERE id = ?
        """, (item[1], item[2], item[3], item[0]))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    
    url = 'https://www.lejobadequat.com/emplois'
    # preload = ''
    job_list = make_joblist_with_url(url, get_content(url))  
    into_csv(job_list)
    into_json(job_list)
    write_into_sql('result.db', job_list)
    read_from_sql('result.db')
    # up_to_date_sql('result.db', data)