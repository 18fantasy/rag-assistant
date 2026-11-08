import json
import random
import importlib.util
根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def 加载(名字, 路径):
    spec = importlib.util.spec_from_file_location(名字, 路径)
    模块 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(模块)
    return 模块
检索模块 = 加载("检索模块", os.path.join(根, "检索.py"))
问答模块 = 加载("问答模块", os.path.join(根, "问答.py"))
全部块 = 检索模块.全部块
问模型 = 问答模块.问模型
拼材料 = 问答模块.拼材料

with open(os.path.join(根, "评测题.json"), encoding="utf-8") as f:
    题目 = json.load(f)

random.seed(42)
随机块 = random.sample(全部块, 3)


def 无材料问答(问题):
    """基线 A：不给材料"""
    材料 = "（本次不提供任何材料）"
    top = [(0.0, 块) for 块 in [{"file": "无", "idx": 0, "text": ""}]]
    return 问答模块.问模型.__wrapped__(问题, top) if hasattr(问答模块.问模型, "__wrapped__") else None


def 用材料问(问题, top):
    return 问模型(问题, top)


行s = []
for 题 in 题目:
    问题 = 题["问题"]
    print(f"第 {题['题号']} 题…", flush=True)
    try:
        # 基线 A：伪造一份空材料，强制它只能靠训练记忆
        空top = [(0.0, {"file": "（无材料）", "idx": 0, "start": 0, "text": "（本题未提供任何材料）"})]
        A = 用材料问(问题, 空top)
    except Exception as e:
        A = f"【出错】{type(e).__name__}: {e}"
    try:
        # 基线 B：随机 3 块
        随机top = [(0.0, 块) for 块 in 随机块]
        B = 用材料问(问题, 随机top)
    except Exception as e:
        B = f"【出错】{type(e).__name__}: {e}"
    行s.append(f"""
## 第 {题['题号']} 题（{题['类型']}）
- 问题：{问题}
- 【基线A·无材料】：{A}
- 【基线B·随机3块】：{B}
- 【标准要点】：{'；'.join(题['要点'])}
""")

with open(os.path.join(根, "基线结果.md"), "w", encoding="utf-8") as f:
    f.write("# 三号评测 · 基线对照（v0.1 同一批 20 题）\n\n- 基线A：不给材料（纯训练记忆）\n- 基线B：随机 3 块（不按相关性）\n- 对照：检索 top-3（正式成绩 16/20）\n" + "\n".join(行s))
print("基线跑完，已写入 基线结果.md")
