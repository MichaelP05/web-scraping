# Ці імпорти необхідні для роботи з відправки e-mails
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json, sqlite3, os, requests, random
from time import sleep
from lxml import html
from bs4 import BeautifulSoup

# Константи
EMAIL =         "example@web.de"
FIRST_NAME =    "Joan"
LAST_NAME =     "Andreas"
PHONE = "01989990000" 
CV_PATH = "C:\\Users\\Mick\\Documents\\*\\Joan_Andreas_Data_Analist_de.pdf"


def send_email(sender_email, sender_password, recipient_email, thema, text, attachments):
    """
    Ця функція власне і відправляє листа
    """
    try:
        # Формування листа
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = thema
        
        # Додаємо текст
        message.attach(MIMEText(text, 'plain'))
        
        # Додаємо вкладення
        for filepath in attachments:
            try:
                with open(filepath, 'rb') as file:
                    filename = filepath.split("\\")[-1]
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={filename}'
                )
                message.attach(part)
            except FileNotFoundError:
                print(f"Файл {filepath} не знайдено.")
        
        # Налаштування SMTP-сервера
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()                               # Увімкнення захищеного з'єднання
            server.login(sender_email, sender_password)     # Авторизація
            server.send_message(message)                    # Відправлення листа
        
        print("Лист успішно відправлено!")
    except Exception as e:
        print(f"Помилка: {e}")

def organizing_mail_distribution():
    """ Для прихованої передачі паролю необхідно задати його через env:
        >>> Win: set EMAIL_PASSWORD=yourpassword
        >>> Linux/Mac: export EMAIL_PASSWORD=yourpassword
    """
    # sender_password = os.getenv('EMAIL_PASSWORD')  # Отримання пароля зі змінної середовища
    # if not sender_password:
    #     raise ValueError("Пароль не знайдено в змінних середовища!")
    
    sender_email = "example@gmail.com"          # Замініть на вашу адресу
    sender_password = "yourpassword"            # Замініть на ваш пароль
    recipient_email = "beischpiel@web.de"       # Замініть на вашу адресу
    thema = "Thema"
    text = "This is the body of the email."
    attachments = ["c:\\Documents\\name.pdf", "c:\\Documents\\name.doc"] # Замініть на ваші файли
    
    send_email(sender_email, sender_password, recipient_email, thema, text, attachments)


def save_user_agents():
    """ 
    Формуємо перелік можливих user-agents, якщо його ще не сформовано
    """
    try:
        # Пробуємо зчитати з кешу 
        with open('user_agents.json', 'r', encoding='utf-8') as f:
            content = f.read()
            print("Перелік юзер агентів вже збережено у файлі")
            
    except FileNotFoundError:
        # Якщо кеш не знайдено, виконуємо HTTP-запит
        response = requests.get(
                'https://hasdata.com/blog/user-agents-for-web-scraping',
            headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                    }
                                )
        tree = html.fromstring(response.text)
        user_agents = tree.xpath("//table[@class='mb-0']/tbody/tr/td[2]/text()")
        
        # print(f"Запит відправлено. Response status code: {response.status_code}")
        if response.status_code == 200:
            # Записуємо результат у файл
            with open('user_agents.json', 'w', encoding='utf-8') as file:
                json.dump(user_agents, file, indent=4)
                print("Дані збережено в кеш.")
        else:
            print("Помилка під час запиту.")
            return ""

def get_my_ip():
    response = requests.get('https://2ip.io/geoip/')
    soup = BeautifulSoup(response.text, 'lxml')
    ip = soup.find('input', {'name': 'ip'})['value']
    print('My current IP Address is:', ip)

    # Це приклад як треба подати дані про проксі-сервер у змінній proxies
    response = requests.get(
        'https://2ip.io/geoip/',
        proxies={'http://123.45.67.89:8080', 'http://123.45.67.89:8080',}
            )
        
    soup = BeautifulSoup(response.text, 'lxml')
    ip = soup.find('input', {'name': 'ip'})['value']
    print('My fake IP Address is:', ip)

class Randomizer:
    """ Цей клас реалізує випадковий вибір user-agent, чи використовуємо проксі...."""
    @staticmethod
    def get_user_agent():
        with open('user_agents.json') as file:
            user_agents = json.load(file)
            user_agent = random.choice(user_agents)
        return user_agent

    @staticmethod
    def get_proxy():
        if random.randint(0, 1):
            return {'http://123.45.67.89:8080', 'http://123.45.67.89:8080', }
        return {}

    @staticmethod
    def get_sleep():
        return random.randint(2, 5)

def parse_xing(urls:list, user_agent: str, proxy: str, sleep_time: int):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")                  # Запуск без інтерфейсу (опціонально)
    options.add_argument(f"user-agent={user_agent}")    # Встановлення User-Agent
    if proxy:                                           # Якщо проксі задано
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    vacancies = []

    for page in urls:
        driver.get(page)
        print(f"Завантажено сторінку: {page}")
        sleep(sleep_time)   # Пауза між запитами
        try:
            # Очікуємо наявність хоча б одного елемента за CSS-селектором
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".results-styles__List-sc-31de7c67-0 > li > article > a")))            
            print("Елементи знайдені!")
        except Exception as e:
            print(f"Помилка очікування елементів на сторінці {page}: {e}")
            continue
        jobs = driver.find_elements(By.CSS_SELECTOR, ".results-styles__List-sc-31de7c67-0 > li > article > a")
        print(f"Знайдено вакансій: {len(jobs)}")
        for job in jobs:
            try:
                url = job.get_attribute('href')     # Отримуємо посилання
                title = job.text                    # Отримуємо текст (назву вакансії)
                vacancies.append({
                    'url'   : url,
                    'title' : title
                })
            except Exception as e:
                print(f"Помилка обробки елементу: {e}")
                continue
    driver.quit()
    # Зберігаємо у вигляді json
    with open('vacancies.json', 'w', encoding="utf-8") as f:
        json.dump(vacancies, f, indent=4)
    # Зберігаємо у вигляді sql
    write_into_sql('vacancies.db', vacancies)
    # Опрацьовуємо отриманий список вакансій
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    process_vacancies(vacancies, EMAIL, FIRST_NAME, LAST_NAME, PHONE, CV_PATH, user_agent, proxy)

def write_into_sql(fn, data: list) -> None:
    # 1. create table
    conn = sqlite3.connect(os.path.join(os.getcwd(), fn))
    cursor = conn.cursor()

    sql = """
        create table if not exists job_list (
            id integer not null primary key,
            title text,
            url text,
            email text,
            is_read boolean default false,
            response_date '0000-00-00' datetime
        )
    """
    cursor.execute(sql)

    # 2. insert data
    
    for item in data:
        
        cursor.execute("""
            insert into job_list (title, url)
            values (?, ?)
        """, (item["title"], item["url"]))

    conn.commit()
    conn.close()


def process_vacancies(vacancies, email, first_name, last_name, phone, cv_path, user_agent: str, proxy: str):
    """
    Ця функція опрацьовує два варіанта подачі даних або шляхом переходу на сторінку того, хто подав обяву 
    та має заповнити необхідні поля або просто надає дані, заповнюючи форми на сайті хing
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Опціонально: запуск без інтерфейсу
    options.add_argument(f"user-agent={user_agent}")  # Встановлення User-Agent
    if proxy:  # Якщо проксі задано
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    for vacancy in vacancies:
        driver.get(vacancy['url'])
        print(f"Відкрито вакансію: {vacancy['title']}")

        try:
            # Сценарій 1: Натиснути кнопку і заповнити форму
            apply_button = wait.until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/section/div/main/div/div/div[1]/div[6]/button[1]')
            ))
            apply_button.click()
            print("Натиснуто кнопку Apply.")

            # Заповнюємо поле e-mail
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-aria8536228911-:r0:"]')))
            email_input.send_keys(email)

            # Натискаємо Continue
            continue_button = driver.find_element(By.CSS_SELECTOR, '.hzUcMy > div:nth-child(1) > span:nth-child(2)')
            continue_button.click()
            print("Натиснуто кнопку Continue (e-mail).")

            # Заповнюємо поля First Name, Last Name, Phone Number
            first_name_input = wait.until(EC.presence_of_element_located((By.NAME, "First Name")))
            first_name_input.send_keys(first_name)

            last_name_input = driver.find_element(By.NAME, "Last Name")
            last_name_input.send_keys(last_name)

            phone_input = driver.find_element(By.NAME, "Phone Number")
            phone_input.send_keys(phone)

            # Натискаємо Continue
            continue_button = driver.find_element(By.XPATH, '//button[contains(text(), "Continue")]')
            continue_button.click()
            print("Натиснуто кнопку Continue (контактні дані).")

        except Exception as e:
            print(f"Сценарій 1 не спрацював: {e}")
            try:
                # Сценарій 2: Перейти на сайт роботодавця
                employer_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(text(), "Visit employer website")]')
                ))
                employer_button.click()
                print("Натиснуто кнопку Visit employer website.")

                # Переходимо на нову сторінку та заповнюємо дані
                wait.until(EC.presence_of_element_located((By.NAME, "E-mail"))).send_keys(email)
                driver.find_element(By.NAME, "Password").send_keys("12345678909")

                # Завантажуємо CV
                upload_button = driver.find_element(By.XPATH, '//button[contains(text(), "Upload CV")]')
                upload_button.click()
                driver.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(cv_path)

                # Натискаємо Register and apply
                register_button = driver.find_element(By.XPATH, '//button[contains(text(), "Register and apply")]')
                register_button.click()
                print("Натиснуто кнопку Register and apply.")

            except Exception as ex:
                print(f"Сценарій 2 не спрацював: {ex}")
                continue

    driver.quit()

if __name__ == '__main__':
    
    urls = ["https://www.xing.com/jobs/search?sc_o=losp_jobs_search_button_click&sc_o_PropActionOrigin=losp_job_search&keywords=Data%20Analyst&location=Leipzig&cityId=2879139.664199&remoteOption=FULL_REMOTE.050e26&employmentType=PART_TIME.58889d*FULL_TIME.ef2fe9&benefit=1.795d28&id=2db317cff8ebbd42be726b3f138a3eac",
            "https://www.xing.com/jobs/search?sc_o=losp_jobs_search_button_click&sc_o_PropActionOrigin=losp_job_search&keywords=Data%20Analyst&location=Leipzig&cityId=2879139.664199&remoteOption=FULL_REMOTE.050e26&employmentType=PART_TIME.58889d*FULL_TIME.ef2fe9&benefit=1.795d28&id=2db317cff8ebbd42be726b3f138a3eac",]
    save_user_agents()

    randomizer = Randomizer()
    u_agent = randomizer.get_user_agent()
    proxy_server = randomizer.get_proxy()
    time = randomizer.get_sleep()
    
    parse_xing(urls, u_agent, proxy_server, time)
