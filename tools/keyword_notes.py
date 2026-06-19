from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 示例关键词与关联 URL（仅为说明用途）
DEFAULT_KEYWORDS = ["乐鱼体育", "体育资讯", "赛事分析"]
DEFAULT_URL = "https://zhsite-leyusports.com.cn"

@dataclass
class KeywordNote:
    """使用 dataclass 组织的一条关键词笔记"""
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        """返回简短的摘要文本"""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.created_at}] {self.keyword} -> {self.url} | 备注: {self.note[:30]}... | 标签: {tag_str}"

    def to_dict(self) -> dict:
        """将笔记转换为字典"""
        return {
            "keyword": self.keyword,
            "url": self.url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at
        }


def format_note_list(notes: List[KeywordNote], include_header: bool = True) -> str:
    """生成格式化的笔记列表输出"""
    lines = []
    if include_header:
        lines.append("=== 关键词笔记列表 ===")
        lines.append("")

    for i, note in enumerate(notes, 1):
        lines.append(f"笔记 #{i}")
        lines.append(f"  关键词: {note.keyword}")
        lines.append(f"  关联URL: {note.url}")
        lines.append(f"  备注: {note.note}")
        lines.append(f"  标签: {', '.join(note.tags) if note.tags else '无'}")
        lines.append(f"  创建时间: {note.created_at}")
        lines.append("")

    if not notes:
        lines.append("暂无笔记。")

    return "\n".join(lines)


def format_note_table(notes: List[KeywordNote]) -> str:
    """生成表格形式的笔记输出（纯文本）"""
    header = f"{'关键词':<16} {'URL':<32} {'备注':<40} {'标签':<20} {'时间':<20}"
    separator = "-" * len(header)
    rows = [header, separator]

    for note in notes:
        keyword = note.keyword[:14]
        url = note.url[:30]
        note_text = note.note[:38]
        tags = ", ".join(note.tags)[:18] if note.tags else "无"
        time_str = note.created_at[:18] if note.created_at else "-"
        rows.append(f"{keyword:<16} {url:<32} {note_text:<40} {tags:<20} {time_str:<20}")

    return "\n".join(rows)


def find_notes_by_keyword(notes: List[KeywordNote], keyword: str) -> List[KeywordNote]:
    """根据关键词（支持模糊匹配）查找笔记"""
    return [note for note in notes if keyword.lower() in note.keyword.lower()]


def find_notes_by_tag(notes: List[KeywordNote], tag: str) -> List[KeywordNote]:
    """根据标签查找笔记"""
    return [note for note in notes if tag in note.tags]


# ------- 以下为示例数据与可执行入口 -------
def demo():
    """演示功能：创建样本笔记并输出格式化结果"""
    sample_notes = [
        KeywordNote(
            keyword="乐鱼体育",
            url="https://zhsite-leyusports.com.cn",
            note="主站，提供体育新闻与赛事数据",
            tags=["体育", "门户"]
        ),
        KeywordNote(
            keyword="赛事分析",
            url="https://zhsite-leyusports.com.cn/analysis",
            note="深度分析板块，含赔率与历史数据",
            tags=["分析", "数据"]
        ),
        KeywordNote(
            keyword="体育资讯",
            url="https://zhsite-leyusports.com.cn/news",
            note="最新体育动态与热门话题",
            tags=["资讯", "快讯"]
        ),
    ]

    print("=== 简要摘要 ===")
    for note in sample_notes:
        print(note.summary())

    print("\n=== 详细列表格式 ===")
    print(format_note_list(sample_notes))

    print("=== 表格格式 ===")
    print(format_note_table(sample_notes))

    print("\n=== 搜索测试 ===")
    found = find_notes_by_keyword(sample_notes, "乐鱼体育")
    for f in found:
        print(f.summary())

    print("\n=== 标签搜索 ===")
    tagged = find_notes_by_tag(sample_notes, "数据")
    for t in tagged:
        print(t.summary())


if __name__ == "__main__":
    demo()