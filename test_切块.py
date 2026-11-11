import importlib.util
import os
这里 = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("三号", os.path.join(这里, "项目三号.py"))
三号 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(三号)
def test_空文件返回空列表(tmp_path):
    空文件 = tmp_path / "空.md"
    空文件.write_text("", encoding="utf-8")
    结果 = 三号.切一个文件(str(空文件), str(tmp_path))
    assert 结果 == []
def test_一个字切出一块(tmp_path):
    文件 = tmp_path / "一个字.md"
    文件.write_text("字", encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    assert len(结果) == 1
    assert 结果[0]["text"] == "字"
    assert 结果[0]["idx"] == 0
    assert 结果[0]["start"] == 0
def test_两个字切出一块(tmp_path):
    文件 = tmp_path / "两个字.md"
    文件.write_text("内容", encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    assert len(结果) == 1
    assert 结果[0]["text"] == "内容"
def test_三百字切一块(tmp_path):
    文件 = tmp_path / "三百字.md"
    文件.write_text("字" * 300, encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    assert len(结果) == 1
    assert len(结果[0]["text"]) == 300
def test_块内四个字段齐全(tmp_path):
    文件 = tmp_path / "字段.md"
    文件.write_text("字" * 600, encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    for 块 in 结果:
        assert set(块.keys()) == {"file", "idx", "start", "text"}
def test_起始位置按步长递增(tmp_path):
    文件 = tmp_path / "步长.md"
    文件.write_text("字" * 600, encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    步长 = 三号.块长 - 三号.重叠
    for i, 块 in enumerate(结果):
        assert 块["idx"] == i
        assert 块["start"] == i * 步长
def test_总字数等于原文加重叠(tmp_path):
    文件 = tmp_path / "字数.md"
    文件.write_text("字" * 600, encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    总字数 = 0
    for 块 in 结果:
        总字数 += len(块["text"])
    重叠重复 = 三号.重叠 * (len(结果) - 1)
    assert 总字数 == 600 + 重叠重复
def test_GBK文件返回None(tmp_path):
    文件 = tmp_path / "gbk.md"
    文件.write_bytes("中文内容".encode("gbk"))
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    assert 结果 is None
def test_建索引跳过坏文件(tmp_path):
    好文件 = tmp_path / "好.md"
    好文件.write_text("正常内容", encoding="utf-8")
    坏文件 = tmp_path / "坏.md"
    坏文件.write_bytes("坏内容".encode("gbk"))
    全部块, 文件数, 跳过数 = 三号.建索引(str(tmp_path))
    assert 文件数 == 2
    assert 跳过数 == 1
    assert len(全部块) >= 1
def test_切块尾巴超过重叠一个字(tmp_path):
    文件 = tmp_path/"切块.md"
    文件.write_text("字"*551, encoding="utf-8")
    结果 = 三号.切一个文件(str(文件), str(tmp_path))
    assert len(结果) == 3
    assert 结果[-1]["start"] + len(结果[-1]["text"]) == 551
