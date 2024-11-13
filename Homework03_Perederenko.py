# import xml.etree.ElementTree as ET
import re
from urllib.parse import urlparse, parse_qs

text = """Welcome to the Regex Training Center! 

01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020. 

(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. 

#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.

"""
def parse_date():
    # date_pattern = r'\b(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b'
    date_pattern = r'\b(?:\d{2}/\d{2}/\d{4}|\d{4}/\d{2}/\d{2}|\d{2}-\d{2}-\d{4}|\d{4}\.\d{2}\.\d{2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})\b'
    """ \d{2}/\d{2}/\d{4} — для формату MM/DD/YYYY, як-от 01/02/2021.
        \d{2}-\d{2}-\d{4} — для формату MM-DD-YYYY, як-от 12-25-2020.
        \d{4}/\d{2}/\d{2} — для формату YYYY/MM/DD, як-от 2021/01/02.
        \d{4}\.\d{2}\.\d{2} — для формату YYYY.MM.DD, як-от 2021.03.15.
        (?:January|February|March|...|December) \d{1,2}, \d{4} — для формату Month DD, YYYY, 
            як-от March 14, 2022. Місяці записуються повністю.
    """
    dates = re.findall(date_pattern, text)
    print(f'Кількість знайдених у тексті дат: {len(dates)}')
    print("Dates:", dates)

def parse_email():
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    print(f'Кількість знайдених у тексті емейлів: {len(emails)}')
    print("Emails:", emails)

def parse_phones():
    phone_pattern = r'\+?\d{1,3}?[ -.]?\(?\d{3}\)?[ -.]?\d{3}[ -.]?\d{4}|\+?\d{1,3}?[ -.]?\d{2,4}[ -.]?\d{3,4}[ -.]?\d{3,4}'

    # Знаходження та форматування всіх номерів
    matches = re.findall(phone_pattern, text)
    formatted_numbers = []

    for match in matches:
        # Видалення всіх нероздільних символів
        clean_number = re.sub(r'[^\d+]', '', match)
        # Додавання номера до списку у бажаному форматі
        formatted_numbers.append(clean_number)
    # phone_pattern = r'(\+?\d{1,3}[ -]?)?(\(?\d{3}\)?[ -.]?)?\d{3}[ -.]?\d{4}'
    """phone_pattern охоплює всі зазначені формати:
        \+?\d{1,3}? — необов'язковий код країни з префіксом +.
        \(?\d{3}\)? — тризначний код регіону в круглих дужках або без них.
        \d{3}[ -.]?\d{4} — основний номер із підтримкою різних роздільників.
        re.sub(r'[^\d+]', '', match) — видаляє всі символи, окрім цифр та знака +, залишаючи лише необхідні цифри.
    """
    print(f'Кількість знайдених у тексті номерів телефонів: {len(formatted_numbers)}')
    print("Phone numbers:", formatted_numbers)

def parse_url():
    # Регулярний вираз для пошуку URL
    url_pattern = r'https?://([a-zA-Z0-9.-]+\.[a-z]{2,6})(/[a-zA-Z0-9._~:/?#[\]@!$&\'()*+,;=%-]*)?'

    # Знаходження всіх URL у тексті
    matches = re.findall(url_pattern, text)

    # Парсинг кожного URL для виділення доменного імені, шляху та параметрів
    parsed_urls = []
    for match in matches:
        domain = match[0]  # Доменне ім'я
        full_path = match[1] if match[1] else ''  # Повний шлях з параметрами, якщо є

        # Використання urlparse для виділення шляху та параметрів
        parsed_url = urlparse("https://" + domain + full_path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)  # Зберігає параметри як словник

        # Додавання до списку результатів
        parsed_urls.append({"url": domain, "path": path, "params": params})

    # Вивід результату
    print(f'Кількість знайдених у тексті номерів URL: {len(parsed_urls)}')
    for item in parsed_urls:
        print("Domain:", item["url"])
        print("Path:", item["path"])
        print("Parameters:", item["params"])
        print()


if __name__ == '__main__':
    # parse_xml()
    
    parse_date()
    parse_email()
    parse_phones()
    parse_url()