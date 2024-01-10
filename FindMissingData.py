import numpy as np
import ipaddress

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