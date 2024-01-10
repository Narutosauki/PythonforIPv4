import requests
import math
import numpy as np
import ipaddress

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


# 读取 ipv4_china.txt 文件
with open("ipv4_china.txt", "r") as ipv4_file:
    ipv4_lines = set(ipv4_file.read().splitlines())

# 读取 IPGroup_.txt 文件
with open("IPGroup_.txt", "r") as ipgroup_file:
    ipgroup_lines = ipgroup_file.read().splitlines()

# 找到相同和不同的行
same_lines = [line for line in ipgroup_lines if line in ipv4_lines]
different_lines = [line for line in ipgroup_lines if line not in ipv4_lines]

# 将相同的行保存到 ipv4_china_extra.txt 文件
with open("ipv4_china_extra.txt", "w") as same_file:
    same_file.write("\n".join(same_lines))

# 将不同的行保存回 IPGroup_.txt 文件
with open("IPGroup_.txt", "w") as ipgroup_file:
    ipgroup_file.write("\n".join(different_lines))

def read_ip_ranges_from_file(file_path):
    with open(file_path, 'r') as file:
        ip_ranges = [line.strip() for line in file.readlines() if line.strip()]
    return ip_ranges

def convert_to_ip_network(ip_range_str):
    return ipaddress.IPv4Network(ip_range_str, strict=False)

def find_non_overlapping_ranges(file_a_ranges, file_b_ranges):
    # 转换为 IPv4Network 对象
    file_a_networks = np.array([convert_to_ip_network(ip_range) for ip_range in file_a_ranges], dtype=object)
    file_b_networks = np.array([convert_to_ip_network(ip_range) for ip_range in file_b_ranges], dtype=object)

    # 使用 NumPy 函数进行比较
    overlaps = np.vectorize(lambda x: any(x.overlaps(b) for b in file_b_networks))
    non_overlapping_ranges = file_a_networks[~overlaps(file_a_networks)]

    return non_overlapping_ranges

# 从文件中读取 IP 地址和子网掩码
file_a_ranges = read_ip_ranges_from_file('ipv4_foreign.txt')
file_b_ranges = read_ip_ranges_from_file('IPGroup_.txt')

# 找出 A 文件中独有的网段
non_overlapping_ranges = find_non_overlapping_ranges(file_a_ranges, file_b_ranges)

# 输出结果到文件
output_file_path = 'ipv4_foreign_extra.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write("缺少的IPv4地址:\n")
    for ip_range in non_overlapping_ranges:
        output_file.write(str(ip_range) + '\n')

# 输出结果行数
print(f"结果已保存到文件: {output_file_path}")
print(f"输出文件中有 {len(non_overlapping_ranges)} 行。")

# 读取 IPGroup_.txt 中的内容
with open('IPGroup_.txt', 'r') as ipgroup_file:
    ipgroup_content = ipgroup_file.read()

# 将结果附加到 IPGroup_.txt 文件
with open('IPGroup_.txt', 'a') as ipgroup_file:
    ipgroup_file.write("\n\n附加的IPv4地址:\n")
    for ip_range in non_overlapping_ranges:
        ipgroup_file.write(str(ip_range) + '\n')

# 输出结果行数
print(f"结果已添加到文件: IPGroup_.txt")
print(f"添加了 {len(non_overlapping_ranges)} 行。")