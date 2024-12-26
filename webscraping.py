import time
import requests
import selectorlib
from sendemail import send_email
import sqlite3

#Establish a connection and cursor
connection=sqlite3.connect("data1_db.db")



URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrap(url):
    """Scrape the page resource from url"""
    response=requests.get(url,headers=HEADERS)
    source=response.text
    return source


def extract(source):
    extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
    value=extractor.extract(source)["tours"]
    return value


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT into events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    Band,city,datetime = row
    cursor = connection.cursor()
    cursor.execute("SELECT * from events where Band = ? and city = ?",(Band,city))
    rows = cursor.fetchall()
    print(rows)
    return rows


"""Running non stop"""
if __name__ == "__main__":
    while True:
        scraped = scrap(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey Saurabh! New event was found")
        time.sleep(2)


