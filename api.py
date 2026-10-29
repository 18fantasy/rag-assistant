import os
import requests
key = os.environ["ZHIPU_API_KEY"]

地址 = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {"Authorization": "Bearer " + key}
body = {
    "model":"glm-4-flash",
    "messages": [{"role": "user", "content": "用一句话解释什么是 RAG"}],
    "max_tokens": 200,
}
try:
    resp = requests.post(地址, json=body, headers=headers, timeout = 30)
    resp.raise_for_status()
    数据 = resp.json()
    print(数据["choices"][0]["message"]["content"])
    print(数据["usage"])
except requests.exceptions.Timeout:
    print("超时：对方没在规定时间内响应，可稍后重试")
except requests.exceptions.ConnectionError:
    print("网络层失败：连不上 / 代理 / SSL，没有收到任何响应")
except requests.exceptions.HTTPError as e:
    状态 = getattr(getattr(e, "response", None), "status_code", "无响应")
    if 状态 == 401 or 状态 == 403:
        print("鉴权失败：检查 ZHIPU_API_KEY 是否有效、有没有多余空格")
    elif 状态 == 429:
        print("限流：对方太忙，等几秒再试（只能等，不能连点）")
    elif 状态 == 400:
        print("请求参数错：检查 model / messages 字段 |", e)
    else:
        print("服务端异常：", 状态, "|", e)
except (KeyError, IndexError) as e:
    print("返回结构不符预期：", type(e).__name__, e, "| 原始响应：", resp.text[:200])
except Exception as e:
    print("没料到的错误：", type(e).__name__, e)

