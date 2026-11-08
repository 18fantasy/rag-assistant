import os
import importlib.util
import requests
这里 =os.path.dirname(os.path.abspath(__file__))
key = os.environ.get("ZHIPU_API_KEY")
if not key:
    print("缺少环境变量 ZHIPU_API_KEY：请先在系统设置，再重开终端/PyCharm")
    raise SystemExit(1)
地址 = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {"Authorization": "Bearer " + key}
spec = importlib.util.spec_from_file_location(
    "检索模块", os.path.join(这里,"检索.py"))
检索模块 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(检索模块)
检索 = 检索模块.检索
def 拼材料(top):
    段 = []
    for i, (分, 块) in enumerate(top, 1):
        段.append(f"[{i}] {块['file']} 第 {块['idx']+1} 块（相关度 {分}）\n{块['text']}")
    return "\n\n".join(段)
def 问模型(问题, top):
    材料 = 拼材料(top)
    messages = [
        {"role": "system", "content": """只依据给定的材料回答。
材料固定为 3 条，编号是 1、2、3。
先把答案写完整（该说的都要说），然后在每句结论后面用 [1] 或 [2] 或 [3] 标出处，格式只许这一种。
材料里找不到答案，就只回答：材料里没有。"""},
        {"role": "user", "content": f"材料：\n{材料}\n\n问题：{问题}"},
    ]
    body = {"model": "glm-4-flash", "messages": messages, "max_tokens": 400, "temperature": 0}
    resp = requests.post(地址, json=body, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
if __name__ == "__main__":
    问题 = "三号现在有哪些已知问题？"
    top = 检索(问题)
    print("\n===== 材料 top-3 =====")
    print(拼材料(top)[:600])
    print("\n===== 答案 =====")
    print(问模型(问题, top))
