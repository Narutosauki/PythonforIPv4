import requests
import math

apnic_url = "http://ftp.apnic.net/stats/apnic/delegated-apnic-latest"
response_apnic = requests.get(apnic_url)
with open("delegated-apnic-latest", "wb") as apnic_file:
    apnic_file.write(response_apnic.content)

# 提取CN和非CN的IPv4信息
with open("delegated-apnic-latest", "r") as apnic_file:
    apnic_lines = apnic_file.readlines()

cn_ipv4_list = [line.split('|') for line in apnic_lines if 'CN' in line and 'ipv4' in line]
foreign_ipv4_list = [line.split('|') for line in apnic_lines if 'CN' not in line and 'ipv4' in line]

cn_ipv4_info = [(ip_info[3], 32 - int(math.log2(int(ip_info[4])))) for ip_info in cn_ipv4_list]
foreign_ipv4_info = [(ip_info[3], 32 - int(math.log2(int(ip_info[4])))) for ip_info in foreign_ipv4_list]

with open("ipv4_china.txt", "w") as china_file:
    for ip, prefix_length in cn_ipv4_info:
        china_file.write(f"{ip}/{prefix_length}\n")

# 从四个网站获取IPv4地址并添加到ipv4_foreign.txt中
foreign_urls = [
    "https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest",
    "https://ftp.ripe.net/ripe/stats/delegated-ripencc-extended-latest",
    "https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest",
    "https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest"
]

with open("ipv4_foreign.txt", "w") as foreign_file:
    
    for ip, prefix_length in foreign_ipv4_info:
        foreign_file.write(f"{ip}/{prefix_length}\n")

    
    for url in foreign_urls:
        response_foreign = requests.get(url)
        foreign_lines = response_foreign.text.split('\n')
        
        foreign_ipv4_list = [line.split('|') for line in foreign_lines if 'ipv4' in line]
        foreign_ipv4_info = [(ip_info[3], 32 - int(math.log2(int(ip_info[4])))) for ip_info in foreign_ipv4_list]

        for ip, prefix_length in foreign_ipv4_info:
            foreign_file.write(f"{ip}/{prefix_length}\n")

with open("ipv4_foreign.txt", "r") as ipv4_foreign_file:
    ipv4_foreign_lines = ipv4_foreign_file.read().splitlines()

# 过滤掉 */17、*/16、*/18 和 */20 行
filtered_lines = [line for line in ipv4_foreign_lines if not line.endswith(('*/17', '*/16', '*/18', '*/20'))]

with open("ipv4_foreign.txt", "w") as ipv4_foreign_file:
    ipv4_foreign_file.write("\n".join(filtered_lines))

