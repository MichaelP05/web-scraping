from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json, sqlite3, os



def parse(urls:list):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без інтерфейсу (опціонально)
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    vacancies = []

    for page in urls:
        driver.get(page)
        print(f"Завантажено сторінку: {page}")
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-Hits-item')))
        except Exception as e:
            print(f"Помилка очікування елементів на сторінці {page}: {e}")
            continue
        jobs = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
        print(f"Знайдено вакансій: {len(jobs)}")
        for job in jobs:
 
            url = job.find_element(By.TAG_NAME,'a' ).get_attribute('href')
            title = job.find_element(By.TAG_NAME, 'h3').text
            # print(f"URL: {url}, Назва: {title}")
            vacancies.append({
                'url': url,
                'title': title
            })

    driver.quit()
    # Зберігаємо у вигляді json
    with open('vacancies.json', 'w', encoding="utf-8") as f:
        json.dump(vacancies, f, indent=4)
    # Зберігаємо у вигляді sql
    write_into_sql('vacancies.db', vacancies)

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
        # print(item["title"],item["url"])
        cursor.execute("""
            insert into job_list (title, url)
            values (?, ?)
        """, (item["title"], item["url"]))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    urls = ["https://jobs.marksandspencer.com/job-search",
            "https://jobs.marksandspencer.com/job-search?country%5B0%5D=United%20Kingdom&page=2&radius=",
            ]
    parse(urls)
    
