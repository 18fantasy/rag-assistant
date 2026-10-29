import os
thing1 = []
块s = []
road = r"C:\Users\2\Desktop\py_road"
for root, dirs, files in os.walk(road):
    dirs[:] = [d for d in dirs if  d not in (".git", "__pycache__", ".venv")]
    for name in files:
        if name.endswith(".md"):
            thing1.append(os.path.join(root, name))
print("找到了", len(thing1), "个.md")
块长 = 300
重叠 = 50
步长 = 块长 - 重叠
road1 = thing1[0]
def 切一个文件(road1):
    块s = []
    with open(road1, "r", encoding="utf-8") as f:
        文本= f.read()
    for 起点 in range(0, len(文本), 步长):
        块s.append({"file":os.path.basename(road1), "idx": len(块s), "text":文本[起点:起点 + 块长]})
    return 块s
全部块 = []
for road1 in thing1:
    全部块.extend(切一个文件(road1))
print("文件", len(thing1), "个,共", len(全部块), "块（块长 300 字，重叠 50 字）")
for 块 in 全部块[0:3]:
    print("-"*60)
    print(f'[{块["idx"]+1}] {块["file"]} 第 {块["idx"]} 块 {len(块["text"])} 字')
    print(块["text"][:80].replace("\n", " "))