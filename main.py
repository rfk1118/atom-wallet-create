import subprocess
import os
import zipfile
import json

# 设置执行次数
n = 10

# 创建一个列表用于存储所有的 funding.address
funding_addresses = []

for index in range(1, n + 1):
    # 执行 npm run cli wallet-init 命令
    subprocess.run(["npm", "run", "cli", "wallet-init"], capture_output=True, text=True)

    # 重命名生成的 wallet.json 文件
    original_file = os.path.join(os.getcwd(), "wallet.json")
    new_file = os.path.join(os.getcwd(), f"wallet{index}.json")
    os.rename(original_file, new_file)

    # 读取新文件中的数据以获取 funding.address
    with open(new_file, "r") as wallet_file:
        wallet_data = json.load(wallet_file)
        if "funding" in wallet_data and "address" in wallet_data["funding"]:
            funding_addresses.append(wallet_data["funding"]["address"])

# 将所有的 funding.address 输出到一个文本文件
with open("funding_addresses.txt", "w") as addresses_file:
    addresses_file.write("\n".join(funding_addresses))

# 打包生成的文件为 ZIP，只打包 wallet 类型文件
with zipfile.ZipFile("wallet_files.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.startswith("wallet") and file.endswith(".json"):
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file), os.getcwd()),
                )

print("操作完成")
