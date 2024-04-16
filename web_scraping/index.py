import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from dateutil.parser import parse
import re

page = requests.get("https://www.republika.co.id/")
obj = BeautifulSoup(page.text, 'html.parser')


f=open('D:\\Scraping Data 1\\Scraping_Data_1\\web_scraping\\headline1.json','w')
data=[]
for headline in obj.find_all('li', class_='list-group-item list-border conten1'):
    judul = headline.find('h3').text if headline.find('h3') else 'Tidak ada judul'
   
    kategori = headline.find('span', class_='kanal-info').text if headline.find('span', class_='kanal-info') else 'Tidak ada kategori'

    waktu_scraping = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Mengambil waktu publish dari elemen dengan class 'date'
    waktu_publish_element = headline.find('div', class_='date')
    waktu_publish_text = waktu_publish_element.text if waktu_publish_element else 'Tidak ada waktu publish'

    # Menggunakan regex untuk mencocokkan pola "X waktu yang lalu"
    waktu_regex = re.search(r'\d+\s\w+\s(?:yang)?\s(?:lalu)', waktu_publish_text)
    
    if waktu_regex:
        waktu_publish = waktu_regex.group()
    else:
        try:
            waktu_publish_parsed = parse(waktu_publish_text)
            # Hitung selisih waktu antara waktu sekarang dan waktu publish
            selisih_waktu = datetime.now() - waktu_publish_parsed
            if selisih_waktu.days > 0:
               time_text = headline.text.strip().split('-')[-1].strip()
            else:
                waktu_publish = f"{selisih_waktu.seconds//3600} jam yang lalu"
        except:
            waktu_publish = 'Format waktu tidak dikenali'


     # Menambahkan judul, kategori, waktu publish, dan waktu scraping sebagai satu entri dictionary
    data.append({
        'judul': judul,
        'kategori': kategori,
        'WP': waktu_publish,
        'WS' : waktu_scraping
        })

jdumps = json.dumps(data, ensure_ascii=False)
f.writelines(jdumps)
f.close()








