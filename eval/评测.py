import sys
import os
import json
import datetime
import importlib.util
def 加载(名字, 路径):
    spec = importlib.util.spec_from_file_location(名字, 路径)
    模块 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(模块)
    return 模块
根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
版本 = sys.argv[1] if len(sys.argv) > 1 else "v0.1"
题库 = {"v0.1": "评测题.json", "v0.2": "评测题_v02.json"}[版本]

检索模块 = 加载("检索模块", 根 + r"\检索.py")
问答模块 = 加载("问答模块", 根 + r"\问答.py")
检索 = 检索模块.检索
问模型 = 问答模块.问模型
with open(根 + "\\eval\\" + 题库, encoding="utf-8") as f:
    包 = json.load(f)
题目 = 包["题目"]
时间 = datetime.datetime.now().strftime("%Y%m%d_%H%M")
行s = []
成功数 = 0
出错数 = 0
for 题 in 题目:
    问题 = 题["问题"]
    print(f"[{版本}] 第 {题['题号']} 题…", flush=True)
    try:
        答案 = 问模型(问题, 检索(问题))
        状态 = "正常"
        成功数 += 1
    except Exception as e:
        状态 = "运行出错"
        错误信息 = f"{type(e).__name__}: {e}"
        出错数 += 1
    if 状态 == "正常":
        中段 = f"- 【状态】：正常\n- 【系统答案】：{答案}"
    else:
        中段 = f"- 【状态】：运行出错（不计分母）\n- 【错误】：{错误信息}"
    行s.append(f"""
## 第 {题['题号']} 题（{题['类型']}）
- 问题：{问题}
{中段}
- 【标准要点】：{'；'.join(题['要点'])}
- 【标准出处】：{题['出处']}
""")

头 = f"""# 跑批原始输出 · 题库 {版本}

- 题库版本：{版本}（{包['题数']} 题：{题库}）
- 跑批时间：{时间}
- 脚本：评测.py ｜ temperature=0 ｜ top-k=3
- 统计：成功 {成功数} / 出错 {出错数}（分母＝成功数）
- 说明：本文件只记原始答案，判定与依据见 `成绩单_{版本}_{时间}.md`
"""
with open(根 + f"\\eval\\跑批原始_{版本}_{时间}.md", "w", encoding="utf-8") as f:
    f.write(头 + "\n".join(行s))
print(f"完成 → 跑批原始_{版本}_{时间}.md（成功 {成功数} / 出错 {出错数}）")
