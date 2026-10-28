"""embodiedalgo_jd044 —— 追溯具身智能算法工程师·线上分布漂移的检测里每一份贡献来自哪里。

统计各来源片段的贡献量与占比，标出具身智能算法工程师·线上分布漂移的检测上最主要的来源

定位：
  贡献占比按字符量算而不是按出现次数，避免长句主导统计

岗位对应：
  目标岗位　百川智能 · 初级具身智能算法工程师
  技能主线　具身智能、PyTorch、强化学习
  领域标签　具身智能

设计约束：
  1. **只报告能定位到具体位置的结论**，不做语义猜测。
  2. **规则表公开**，每条命中都能对应到岗位要求的一条明示规则。
  3. **输入为空或格式不对时明确报错**，不静默返回空结果。

仅依赖 Python 标准库。

用法:
    python embodiedalgo_jd044.py --help
    python embodiedalgo_jd044.py --file input.txt
    python embodiedalgo_jd044.py --text "示例内容"
    python embodiedalgo_jd044.py --file input.txt --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# 岗位规则表：每条规则独立可核查，命中即报，不做推断。
# 规则由岗位 JD 的技能线与领域标签派生——每条都能对回岗位要求。
# 目标岗位：百川智能 · 初级具身智能算法工程师
RULES: list[dict] = [
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·缺失",
        "why": "岗位要求「具身智能」在输入里找不到对应内容",
        "severity": "high",
        "keywords": ['missing', 'absent', '缺少', '没有', '未提供', '具身智能'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·冲突",
        "why": "两处关于「PyTorch」的描述互相矛盾",
        "severity": "high",
        "keywords": ['conflict', 'contradict', '矛盾', '不一致', '相反', 'PyTorch'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·越界",
        "why": "「强化学习」的取值超出岗位场景的常规范围",
        "severity": "medium",
        "keywords": ['out of range', 'outlier', '越界', '超限', '超过', '强化学习'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·退化",
        "why": "「具身智能算法工程师」相关的信息量不足以支撑判断",
        "severity": "medium",
        "keywords": ['degrade', 'insufficient', '不足', '太少', '无法', '具身智能算法工程师'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·泄漏#2",
        "why": "「具身智能」相关的内容被意外暴露",
        "severity": "high",
        "keywords": ['leak', 'expose', '泄漏', '暴露', '明文', '具身智能'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·重复#2",
        "why": "同一处「PyTorch」信息被反复传递",
        "severity": "low",
        "keywords": ['duplicate', 'repeat', '重复', 'again', 'PyTorch'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·陈旧#2",
        "why": "「强化学习」的时效性已过期",
        "severity": "medium",
        "keywords": ['stale', 'expired', '过期', '陈旧', '旧版', '强化学习'],
    },
    {
        "name": "具身智能算法工程师·线上分布漂移的检测·不可核#2",
        "why": "关于「具身智能算法工程师」的说法无法追溯到具体证据",
        "severity": "high",
        "keywords": ['unverifiable', 'no evidence', '无法追溯', '没有来源', '具身智能算法工程师'],
    },
]


def embodiedalgo_jd044_read_numbers(text: str) -> list[float]:
    return [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", text.replace(",", ""))]


def embodiedalgo_jd044_analyze(text: str) -> dict:
    """主分析：来源与占比。"""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if not blocks:
        return {"ok": False, "error": "没有内容", "count": 0}
    total = sum(len(b) for b in blocks)
    parts = []
    for i, b in enumerate(blocks):
        head = b.splitlines()[0][:60] if b.splitlines() else "(空)"
        parts.append({"index": i, "head": head, "size": len(b),
                      "share": round(len(b) / total, 4) if total else 0.0})
    return {
        "ok": True,
        "count": len(blocks),
        "total_size": total,
        "parts": parts,
        "largest": max(parts, key=lambda p: p["size"])["head"],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def render(result: dict) -> str:
    """把结果渲染成人读的文本。每个工具的版式不同。"""
    out: list[str] = []
    if not result.get("ok", True):
        out.append(f"无法分析：{{result.get('error', '未知原因')}}")
        return "\n".join(out)
    out.append(f"片段数：{result['count']}  总量 {result['total_size']}")
    out.append("")
    for p_ in result["parts"]:
        out.append(f"  {p_['share']:>7.2%}  {p_['size']:>6}  {p_['head']}")
    out.append("")
    out.append(f"最大来源：{result['largest']}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="embodiedalgo_jd044",
        description="统计各来源片段的贡献量与占比，标出具身智能算法工程师·线上分布漂移的检测上最主要的来源（仅依赖标准库）",
        epilog=(
            "示例:\n"
            "  python embodiedalgo_jd044.py --file input.txt\n"
            "  python embodiedalgo_jd044.py --text '示例内容'\n"
            "  python embodiedalgo_jd044.py --file input.txt --json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="输入文件路径")
    src.add_argument("--text", help="直接给出输入内容")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            print(f"读不了文件：{{e}}", file=sys.stderr)
            return 2
    else:
        content = args.text

    if not content.strip():
        print("输入是空的。", file=sys.stderr)
        return 2

    result = embodiedalgo_jd044_analyze(content)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(render(result))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
