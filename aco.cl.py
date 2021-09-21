import csv
import threading

from bs4 import BeautifulSoup
from requests import get

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                  "Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}

website = "https://aco.cl/"
buscador = f'{website}action/resources/buscador.php?value='
threadcount = 10
semaphore = threading.Semaphore(threadcount)
lock = threading.Lock()


def scrape(line):
    semaphore.acquire()
    href = BeautifulSoup(get(f'{buscador}{line}').content, 'lxml').find('a')['href']
    soup = BeautifulSoup(get(f"{website}{href}").content, 'lxml')
    price = soup.find('div', {'class': 'precio'}).text.strip().split(" ")[0]
    data = [line, price]
    for img in soup.find('div', {'id': 'pager-ext'}).find_all('img'):
        if "video.png" not in img['src']:
            data.append(f"{website}{img['src']}".strip())
    for a in soup.find('div', {'id': 'pager-ext'}).find_all('a'):
        data.append(f"{a['href']}".strip())
    print(data)
    append(data)
    semaphore.release()


def append(row):
    with lock:
        with open('aco.cl.csv', 'a+') as file:
            csv.writer(file).writerow(row)


def main():
    with open('todoslossku.txt', 'r') as file:
        lines = file.read().splitlines()
    for line in lines[1:]:
        threading.Thread(target=scrape, args=(line,)).start()


if __name__ == "__main__":
    main()
