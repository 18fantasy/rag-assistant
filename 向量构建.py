
import os
import time
import requests
import json
import importlib.util
这里 = os.path.dirname(os.path.abspath(__file__))
def 加载(名字, 路径):
    spec = importlib.util.spec_from_file_location(名字, 路径)
    模块 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(模块)
    return 模块
检索模块 = 加载("检索模块", os.path.join(这里, "检索.py"))
全部块 = 检索模块.全部块
key = os.environ.get("ZHIPU_API_KEY")
if not key:
    raise RuntimeError("缺少环境变量 ZHIPU_API_KEY：请先在系统设置，再重开终端/PyCharm")
头部 = {"Authorization": "Bearer " + key}
地址 = "https://open.bigmodel.cn/api/paas/v4/embeddings"
def 调embedding(文本列表):
    resp = requests.post(地址, json={"model": "embedding-3", "input": 文本列表},
                         headers=头部, timeout=60)
    resp.raise_for_status()
    return [item["embedding"] for item in resp.json()["data"]]
文本列表 = [块["text"] for 块 in 全部块]
试通模式 = False
if 试通模式:
    文本列表 = 文本列表[:10]
    print("【试通模式】只跑前 10 条")
print(f"共 {len(文本列表)} 块，开始建向量…")
全部向量 = []
批大小 = 10
for i in range(0, len(文本列表), 批大小):
    一批 = 文本列表[i : i + 批大小]
    向量s = None
    for 尝试 in range(1, 3):
        try:
            向量s = 调embedding(一批)
            break
        except requests.exceptions.RequestException as e:
            if 尝试 == 2:
                print(f"一批两次都失败：{type(e).__name__}: {e}")
                print("停在这里。落盘前不许有洞——修好网络后重跑脚本")
                raise
            print(f"一批失败（{type(e).__name__}），2 秒后重试")
            time.sleep(2)
    全部向量.extend(向量s)
    print(f"进度 {len(全部向量)}/{len(文本列表)}")
with open(os.path.join(这里, "向量.json"), "w", encoding="utf-8") as f:
    json.dump(全部向量, f, ensure_ascii=False)
print(f"落盘完成：{len(全部向量)} 个向量")
