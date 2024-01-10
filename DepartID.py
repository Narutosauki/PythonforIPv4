import ipaddress

def split_ip_addresses(input_file, cidr_file, ip_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cidr_addresses = []
    ip_addresses = []

    for line in lines:
        line = line.strip()
        if '/' in line:  # CIDR形式
            cidr_addresses.append(line)
        else:  # 具体地址
            ip_addresses.append(line)

    # 写入CIDR形式的IP地址范围到文件
    with open(cidr_file, 'w') as cidr_output:
        for cidr_address in cidr_addresses:
            cidr_output.write(f"{cidr_address}\n")

    # 写入具体地址到文件
    with open(ip_file, 'w') as ip_output:
        for ip_address in ip_addresses:
            ip_output.write(f"{ip_address}\n")

# 使用示例
split_ip_addresses('IPGroup_ios.txt', 'CIDR_addresses.txt', 'IP_addresses.txt')
