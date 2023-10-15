from bs4 import BeautifulSoup
import sys
from operator import itemgetter
import csv
import requests

if len(sys.argv) != 3:
    print("Zadej 3 argumenty")
else:  
    odkaz_webu = sys.argv[1]
    jmeno_souboru = sys.argv[2]
    
    original_url = odkaz_webu

    response = requests.get(original_url)
    soup_url = BeautifulSoup(response.text, "html.parser")
    url_list = []
    for i in soup_url.find_all("a"):
        href = i.get("href")
        url_list.append(href)
    
    url_na_header = str("https://volby.cz/pls/ps2017nss/"+url_list[5])

    kod_obce = []
    for i in soup_url.find_all("td", class_ = "cislo"):
        kod_obce.append(i.text)

    nazev_obce = []
    for i in soup_url.find_all("td", class_ = "overflow_name"):
        nazev_obce.append(i.text)

    response = requests.get(url_na_header)
    soup = BeautifulSoup(response.text, "html.parser")

    strany = []
    for td in soup.find_all("td", class_ = "overflow_name"):
        strany.append(td.text)

    header0 = ["code", "location", "registered", "envelopes", "valid"]
    header = header0 + strany

    stats = []
    for td in soup.find_all("td", class_ = "cislo"):
        stats.append(td.text)
    for i in range(len(stats)):
        cleaned_value = stats[i].replace("\xa0", " ")
        stats[i] = cleaned_value
    potrebne_stats = list(itemgetter(3,6,7)(stats))

    celkem_hlasy = []
    for td in soup.find_all("td", class_ = "cislo"):
        celkem_hlasy.append(td)
    hlasy_stran = []
    for td in celkem_hlasy[10::3]:
        hlasy_stran.append(td.text)
    for i in range(len(hlasy_stran)):
        cleaned_value = hlasy_stran[i].replace("\xa0", " ")
        hlasy_stran[i] = cleaned_value

    response = requests.get(original_url)
    soup = BeautifulSoup(response.text, "html.parser")

    href_list = []
    for link in soup.find_all("a"):
        href = link.get("href")
        href_list.append(href)

    href_list = href_list[5:-2:2]
    n = 0
    rows = []
    for link in href_list:    
        response0 = requests.get("https://volby.cz/pls/ps2017nss/" + str(href_list[int(n)]))
        soup = BeautifulSoup(response0.text, "html.parser")
        table = soup.find("table", {"class": "table"})
        td_elements = table.find_all("tr")

        stats = []
        for td in soup.find_all("td", class_ = "cislo"):
            stats.append(td.text)
        for i in range(len(stats)):
            cleaned_value = stats[i].replace("\xa0", " ")
            stats[i] = cleaned_value
        potrebne_stats = list(itemgetter(3,6,7)(stats))

        celkem_hlasy = []
        for td in soup.find_all("td", class_ = "cislo"):
            celkem_hlasy.append(td)
        hlasy_stran = []
        for td in celkem_hlasy[10::3]:
            hlasy_stran.append(td.text)
        for i in range(len(hlasy_stran)):
            cleaned_value = hlasy_stran[i].replace("\xa0", " ")
            hlasy_stran[i] = cleaned_value

        row = potrebne_stats + hlasy_stran
        rows.append(row)
        n += 1

    list0 = []

    for val1, val2, sublist3 in zip(kod_obce, nazev_obce, rows):
        new_sublist = [val1, val2] + sublist3
        list0.append(new_sublist)

    with open(jmeno_souboru, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for value in list0:
            writer.writerow(value)