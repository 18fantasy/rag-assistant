import os
import importlib.util
import requests
import logging
import time
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
不该重试 = (400, 401, 403, 404)
这里 =os.path.dirname(os.path.abspath(__file__))
地址 = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
def 取头部():
    key = os.environ.get("ZHIPU_API_KEY")
    if not key:
        raise RuntimeError("缺少环境变量 ZHIPU_API_KEY：请先在系统设置，再重开终端/PyCharm")
    return {"Authorization": "Bearer " + key}
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
材料里出现的数字、文件名、日期，必须原样照抄，不许改写或四舍五入；材料里没有的数字、文件名、结论，一律不许出现在答案里。
材料里找不到答案，就只回答：材料里没有。"""},
        {"role": "user", "content": f"材料：\n{材料}\n\n问题：{问题}"},
    ]
    body = {"model": "glm-4-flash", "messages": messages, "max_tokens": 400, "temperature": 0}
    for 第几次 in range(1, 4):
        try:
            resp = requests.post(地址, json=body, headers=取头部(), timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError :
            if resp.status_code in 不该重试:
                logging.error("HTTP %s：这个错重试也没用，直接退出", resp.status_code)
                raise
            if 第几次 == 3 :
                logging.error("第 %d 次仍失败：HTTP %s，放弃", 第几次, resp.status_code)
                raise
            logging.warning("第 %d 次失败：HTTP %s，%d 秒后重试",
                            第几次, resp.status_code, 第几次 * 2)
        # 分两个 except：HTTPError 才有 resp.status_code 能判断该不该重试；
        # 连接类错误没有 resp，只能一律重试。合并会读到上一轮的旧状态码。
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as 错误:
            if 第几次 == 3:
                logging.error("第 %d 次仍失败：%s，放弃", 第几次, type(错误).__name__)
                raise
            logging.warning("第 %d 次失败：%s，%d 秒后重试",
                            第几次, type(错误).__name__, 第几次 * 2)
        time.sleep(第几次 * 2)
if __name__ == "__main__":
    问题 = "三号现在有哪些已知问题？"
    top = 检索(问题)
    print("\n===== 材料 top-3 =====")
    print(拼材料(top)[:600])
    print("\n===== 答案 =====")
    print(问模型(问题, top))
