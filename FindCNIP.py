# 读取 ipv4.txt 文件
with open("ipv4_china.txt", "r") as ipv4_file:
    ipv4_lines = set(ipv4_file.read().splitlines())

# 读取 IPGroup_.txt 文件
with open("IPGroup_.txt", "r") as ipgroup_file:
    ipgroup_lines = set(ipgroup_file.read().splitlines())

# 获取相同的行
same_lines = ipv4_lines.intersection(ipgroup_lines)

# 将结果保存到 same.txt 文件
with open("same.txt", "w") as same_file:
    same_file.write("\n".join(same_lines))
