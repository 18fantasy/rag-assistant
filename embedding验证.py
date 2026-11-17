import os
import requests
地址 = "https://open.bigmodel.cn/api/paas/v4/embeddings"
key = os.environ.get("ZHIPU_API_KEY")
if not key:
    raise RuntimeError("缺少环境变量 ZHIPU_API_KEY：请先在系统设置，再重开终端/PyCharm")

头部 = {"Authorization": "Bearer " + key}
body = {
    "model": "embedding-3",
    "input": "三号第一次跑通切块器时，切了多少个文件、多少块？",
}
resp = requests.post(地址, json=body, headers=头部, timeout=30)
print("状态码:", resp.status_code)

if resp.status_code == 200:
    数据 = resp.json()
    向量 = 数据["data"][0]["embedding"]
    print("向量维度:", len(向量))
    print("前 5 个分量:", 向量[:5])
else:
    print("接口没通。响应原文（前 600 字）如下，贴给老师看：")
    print(resp.text[:600])
