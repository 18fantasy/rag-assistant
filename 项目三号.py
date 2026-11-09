import os
根目录 = os.environ.get("RAG_ROOT", r"C:\Users\2\Desktop\py_road")
def 扫文件(根目录):
    thing1 = []
    for root, dirs, files in os.walk(根目录):
        跳过 = (".git", "__pycache__", ".venv", "_backup", "_drafts", "eval")
        dirs[:] = [d for d in dirs if d not in 跳过 and "_旧_" not in d and "作废" not in d]
        for name in files:
            if name.endswith(".md"):
                thing1.append(os.path.join(root, name))
    return thing1
块长 = 300
重叠 = 50
步长 = 块长 - 重叠
def 切一个文件(路径, 根目录):
    块s = []
    with open(路径, "r", encoding="utf-8") as f:
        文本= f.read()
    for 起点 in range(0, len(文本), 步长):
        块s.append({"file":os.path.relpath(路径,根目录), "idx": len(块s), "start":起点, "text":文本[起点:起点 + 块长]})
    return 块s
def 建索引(根目录):
    thing1 = 扫文件(根目录)
    全部块 = []
    for 路径 in thing1:
        全部块.extend(切一个文件(路径, 根目录))
    return 全部块, len(thing1)
if __name__ == "__main__":
    全部块, 文件数 = 建索引(根目录)
    print(f"文件 {文件数}个 共{len(全部块)}块 块(块长{块长}字, 重叠{重叠}字)")
    for 块 in 全部块[0:3]:
        print("-"*60)
        print(f'[{块["idx"]+1}] {块["file"]} 第 {块["idx"]} 块 {len(块["text"])} 字')
        print(块["text"][:80].replace("\n", " "))