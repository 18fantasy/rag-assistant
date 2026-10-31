import importlib.util
import math
spec = importlib.util.spec_from_file_location(
    "三号", r"C:/Users/2/Desktop/py_road/projects/rag-assistant/项目三号.py")
三号 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(三号)
全部块 = 三号.全部块
print("载入块数:", len(全部块))
停用 = {"多少", "一共", "什么", "怎么", "是哪", "哪些", "这个", "可以", "如何", "为什", "么算", "计怎"}
def 切片段(问题):
    return [问题[i:i+2] for i in range(len(问题) - 1) if 问题[i:i+2] not in 停用]
def 建权重(片段s):
    权重 = {}
    for 片 in 片段s:
        df = sum(1 for 块 in 全部块 if 片 in 块["text"])
        if df ==0:
            continue
        权重[片] = math.log(len(全部块) / (1 + df))
    return 权重
def 检索(问题, k=3):
    片段s = 切片段(问题)
    权重 = 建权重(set(片段s))
    表 = []
    for 块 in 全部块:
        分 = sum(权重[片] for 片 in 片段s if 片 in 块["text"])
        表.append((round(分, 2), 块))
    表.sort(key=lambda x: x[0], reverse=True)
    结果, 见过 = [], set()
    for 分, 块 in 表:
        键 = (块["file"], 块["idx"])
        if 键 in 见过:
            continue
        见过.add(键)
        结果.append((分, 块))
        if len(结果) == k:
            break
    return 结果
for 问题 in ["三号切块一共多少块？块长多少？", "记账本的月度统计怎么算"]:
    print(f"\n=== {问题} ===")
    for 分, 块 in 检索(问题):
        print(f'{分:7.2f}  {块["file"]} 第 {块["idx"]+1} 块')
        print("      ", 块["text"][:60].replace("\n", " "))
