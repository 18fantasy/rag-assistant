import json
import importlib.util
def 加载(名字, 路径):
    spec = importlib.util.spec_from_file_location(名字, 路径)
    模块 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(模块)
    return 模块
检索模块 = 加载("检索模块", r"C:/Users/2/Desktop/py_road/projects/rag-assistant/检索.py")
问答模块 = 加载("问答模块", r"C:/Users/2/Desktop/py_road/projects/rag-assistant/问答.py")
检索 = 检索模块.检索
问模型 = 问答模块.问模型
with open(r"C:/Users/2/Desktop/py_road/projects/rag-assistant/评测题.json", encoding="utf-8") as f:
    题目 = json.load(f)
行s = []
for 题 in 题目:
    问题 = 题["问题"]
    print(f"第 {题['题号']} 题跑中…", flush=True)
    try:
        top = 检索(问题)
        答案 = 问模型(问题, top)
    except Exception as e:
        答案 = f"【运行出错】{type(e).__name__}: {e}"
    行s.append(f"""
## 第 {题['题号']} 题（{题['类型']}）
- 问题：{问题}
- 【系统答案】：{答案}
- 【标准要点】：{'；'.join(题['要点'])}
- 【标准出处】：{题['出处']}
- 你的判定：（对 / 错 / 出处错 / 拒答对 / 拒答错）
""")
with open(r"C:/Users/2/Desktop/py_road/projects/rag-assistant/评测结果.md", "w", encoding="utf-8") as f:
    f.write("# 三号评测 · 对照表（v0 首轮）\n\n跑完后逐题在「你的判定」里填：对 / 错 / 出处错 / 拒答对 / 拒答错\n" + "\n".join(行s))
print("全部跑完，结果已写入 评测结果.md")
