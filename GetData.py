import requests
import re
from math import log2

def process_rir_data(url, country_code):
    response = requests.get(url)
    data = response.text
    
    ipv4_entries = re.findall(rf'{country_code}\|ipv4\|(.+?)\|(\d+?)\|', data)
    ipv4_addresses = [f"{ip}/{32 - int(log2(int(size)))}" for ip, size in ipv4_entries]
    
    return ipv4_addresses

urls = [
    ("https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest", "US"),
    ("https://ftp.ripe.net/ripe/stats/delegated-ripencc-extended-latest", "EU"),
    ("https://ftp.apnic.net/stats/apnic/delegated-apnic-extended-latest", "CN"),
    ("https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest", "LA"),
    ("https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest", "AF")
]

china_ipv4_addresses = []
foreign_ipv4_addresses = []
for url, country_code in urls:
    ipv4_addresses = process_rir_data(url, country_code)
    
    if country_code == "CN":
        china_ipv4_addresses.extend(ipv4_addresses)
    else:
        foreign_ipv4_addresses.extend(ipv4_addresses)

# 保存中国IP
with open("ipv4_china.txt", "w") as china_file:
    china_file.write("\n".join(china_ipv4_addresses))

# 保存其他国家IP
with open("ipv4_foreign.txt", "w") as foreign_file:
    foreign_file.write("\n".join(foreign_ipv4_addresses))
