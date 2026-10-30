import requests
import os
key = os.environ["ZHIPU_API_KEY"]
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {"Authorization": "Bearer " + key}
with open(r"C:\Users\2\Desktop\py_road\进度.md","r", encoding = "utf-8") as f:
    文本 = f.read()
    段落们 = 文本.split("\n\n")
    命中 = [d for d in 段落们 if "4799" in d]
    材料 = 命中[0] if 命中 else ""
问题 = "项目三号第1步是哪天跑通的？切成了多少块？块长和重叠是多少？"
def 问(问题, 材料 = None):
    if 材料:
        messages = [
            {"role":"system", "content":"只根据我提供的材料回答， 材料里没有就说不知道。"},
            {"role":"user", "content":f"材料:\n{材料}\n\n问题: {问题}"},
        ]
    else:
        messages = [{"role":"user", "content":问题}]
    body = {"model":"glm-4-flash", "messages":messages, "max_tokens":300}
    resp = requests.post(url, json=body, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
print("\n=== A 不给材料 ===")
print(问(问题))
print("\n=== B 给材料 ===")
print(问(问题, 材料))

