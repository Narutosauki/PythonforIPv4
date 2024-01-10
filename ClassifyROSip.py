import numpy as np
import ipaddress

def read_ip_ranges_from_file(file_path):
    with open(file_path, 'r') as file:
        ip_ranges = [line.strip() for line in file.readlines() if line.strip()]
    return ip_ranges

def convert_to_ip_network(ip_range_str):
    return ipaddress.IPv4Network(ip_range_str, strict=False)

def classify_ip_ranges(ip_ranges, foreign_ranges, china_ranges):
    foreign_networks = np.array([convert_to_ip_network(ip_range) for ip_range in foreign_ranges], dtype=object)
    china_networks = np.array([convert_to_ip_network(ip_range) for ip_range in china_ranges], dtype=object)

    classified_foreign = []
    classified_china = []

    for ip_range in ip_ranges:
        ip_network = convert_to_ip_network(ip_range)
        if any(ip_network.overlaps(foreign) for foreign in foreign_networks):
            classified_foreign.append(ip_range)
        elif any(ip_network.overlaps(china) for china in china_networks):
            classified_china.append(ip_range)

    return classified_foreign, classified_china

# 从文件中读取 IP 地址和子网掩码
remaining_ip_ranges = read_ip_ranges_from_file('剩余ip.txt')
foreign_ranges = read_ip_ranges_from_file('ipv4_foreign.txt')
china_ranges = read_ip_ranges_from_file('ipv4_china.txt')

# 进行分类
foreign_ip, china_ip = classify_ip_ranges(remaining_ip_ranges, foreign_ranges, china_ranges)

# 输出结果到文件
output_foreign_path = 'foreign_ip.txt'
with open(output_foreign_path, 'w') as output_file:
    output_file.write("国外IP地址:\n")
    for ip_range in foreign_ip:
        output_file.write(str(ip_range) + '\n')

output_china_path = 'china_ip.txt'
with open(output_china_path, 'w') as output_file:
    output_file.write("国内IP地址:\n")
    for ip_range in china_ip:
        output_file.write(str(ip_range) + '\n')

# 输出结果行数
print(f"国外IP地址已保存到文件: {output_foreign_path}")
print(f"国内IP地址已保存到文件: {output_china_path}")
print(f"国外IP文件中有 {len(foreign_ip)} 行。")
print(f"国内IP文件中有 {len(china_ip)} 行。")
