import  importlib.util
块们 = [
    {"file": "进度.md",     "idx": 0, "text": "项目三号第 1 步切块器跑通，180 个 md 切成 4799 块，块长 300 重叠 50。"},
    {"file": "交接便笺.md",  "idx": 0, "text": "WorkBuddy 与老师之间的传话通道，只追加不删，一行一条。"},
    {"file": "技术债清单.md", "idx": 0, "text": "v0 能跑但不稳的 13 条，v1 统一改，P0 七条挡住服务化。"},
    {"file": "踩坑素材库.md", "idx": 0, "text": "真实报错原文、根因、改法、可迁移结论，写博客时直接取。"},
    {"file": "职业路线图.md", "idx": 0, "text": "2026-10 到 2027-06 的阶段目标，2027 暑期实习是硬指标。"},
]
问题 = "三号切块一共多少块？块长多少？"
def 打分(问题, 块):
    分数 = 0
    for i in range(len(问题)-1):
        片段 = 问题[i:i+2]
        if 片段 in 块["text"]:
            分数 += 1
    return 分数
print("=== 第 1 段：手工 5 块 ===")
for 块 in 块们:
    print(f'{打分(问题, 块):3d}  {块["file"]}')
spec = importlib.util.spec_from_file_location(
    "三号",r"C:\Users\2\Desktop\py_road\projects\rag-assistant\项目三号.py"
)
三号 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(三号)
全部块 = 三号.全部块
print("载入块数:", len(全部块))
分数表 = [(打分(问题, 块), 块) for 块 in 全部块]
分数表.sort(key=lambda x: x[0], reverse=True)
print("\n=== top 3 ===")
for 分, 块 in 分数表[:3]:
     print(f'{分:4d}  {块["file"]} 第 {块["idx"]} 块')
     print("      ", 块["text"][:60].replace("\n", " "))
