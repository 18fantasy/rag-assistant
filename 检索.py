import importlib.util
import math
import os
import json
import requests
地址 = "https://open.bigmodel.cn/api/paas/v4/embeddings"
key = os.environ.get("ZHIPU_API_KEY")
if not key :
    raise RuntimeError("缺少环境变量 ZHIPU_API_KEY：请先在系统设置，再重开终端/PyCharm")
头部 = {"Authorization": "Bearer " + key}
这里 = os.path.dirname(os.path.abspath(__file__))
向量路径 = os.path.join(这里,"向量.json")
if os.path.exists(向量路径):
    with open(向量路径, "r", encoding="utf-8") as f:
        全部向量 = json.load(f)
    print(f"从落盘向量载入{len(全部向量)}个")
else:
    print(f"向量.json不存在:先跑python向量构建.py")
spec = importlib.util.spec_from_file_location(
    "三号", os.path.join(这里, "项目三号.py"))
三号 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(三号)
索引路径 = os.path.join(这里, "索引.json")
if os.path.exists(索引路径):
    with open(索引路径, "r", encoding="utf-8") as f:
        全部块 = json.load(f)
        print(f"从落盘索引载入{len(全部块)}块")
else:
    全部块 = 三号.建索引(三号.根目录)[0]
    with open(索引路径, "w", encoding="utf-8") as f:
        json.dump(全部块, f, ensure_ascii=False)
    print(f"重建索引{len(全部块)}块，已落盘")
def 调embedding(文本列表):
    resp = requests.post(地址,json = {"model":"embedding-3", "input":文本列表 }, headers = 头部, timeout=60)
    resp.raise_for_status()
    return[item["embedding"]for item in resp.json()["data"]]
def 问题向量(问题):
    return 调embedding([问题])[0]
def 余弦(a, b):
    点积 = sum(x*y for x, y in zip(a, b))
    模a = sum(x*x for x in a) ** 0.5
    模b = sum(x*x for x in b) ** 0.5
    return 点积 / (模a * 模b)
def 向量打分(问题):
    q = 问题向量(问题)
    return [余弦(q, v) for v in 全部向量]
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
def 字面打分(问题):
    片段s = 切片段(问题)
    权重 = 建权重(set(片段s))
    表 = []
    for 块 in 全部块:
        分 = sum(权重[片] for 片 in 片段s if 片 in 块["text"])
        表.append((分, 块))
    return 表
def 检索(问题, k=3):
    表 = 字面打分(问题)
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
def 检索混合(问题, k=3):
    字面表 = 字面打分(问题)
    向量分 = 向量打分(问题)
    最大字面 = max(s for s, 块 in 字面表)
    表 = []
    for i, (字面s, 块) in enumerate(字面表):
        字面归一 = 字面s / 最大字面 if 最大字面 > 0 else 0
        向量归一 = (向量分[i] + 1) / 2
        总分 = 0.5 * 字面归一 + 0.5 * 向量归一
        表.append((总分, 块))
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
if __name__ == "__main__":
    for 问题 in ["三号切块一共多少块？块长多少？", "记账本的月度统计怎么算"]:
        print(f"\n=== {问题} ===")
        for 分, 块 in 检索混合(问题):
            print(f'{分:7.2f}  {块["file"]} 第 {块["idx"]+1} 块')
            print("      ", 块["text"][:60].replace("\n", " "))
