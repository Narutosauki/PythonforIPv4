# 读取 ipv4_china.txt 文件
with open("ipv4_china.txt", "r") as ipv4_file:
    ipv4_lines = set(ipv4_file.read().splitlines())

# 读取 IPGroup_.txt 文件
with open("IPGroup_.txt", "r") as ipgroup_file:
    ipgroup_lines = ipgroup_file.read().splitlines()

# 找到相同和不同的行
same_lines = [line for line in ipgroup_lines if line in ipv4_lines]
different_lines = [line for line in ipgroup_lines if line not in ipv4_lines]

# 将相同的行保存到 extra_china.txt 文件
with open("extra_china.txt", "w") as same_file:
    same_file.write("\n".join(same_lines))

# 将不同的行保存回 IPGroup_.txt 文件
with open("IPGroup_.txt", "w") as ipgroup_file:
    ipgroup_file.write("\n".join(different_lines))

