#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sw_lifecycle.py — IEC 62304 医疗器械软件生命周期工具
====================================================
软件安全等级判定（Class A/B/C）+ 生命周期过程清单 + SOUP 登记检查点。

分级依据（IEC 62304:2006+A1:2015 §4.3）：
  A — 不可能导致/促成伤害
  B — 可能导致非严重伤害
  C — 可能导致死亡或严重伤害（按**严重度**判定，不问概率）
过程清单按官方条款编号（§5.1–5.8 开发 / §6 维护 / §7 风险管理 /
§8 配置管理 / §9 问题解决；2026-10-12 复审修订，原 5–13 连续编号有误）。
诚实边界：最终等级须结合风险管理文件（ISO 14971）输出判定。
"""
from __future__ import annotations
import argparse
import sys

SW_PROCESSES = [
    ("5.1 软件开发策划", "软件安全等级定义/开发计划/维护计划/风险管理衔接"),
    ("5.2 软件需求分析", "软件需求来自系统需求；安全分类需求可追溯"),
    ("5.3 软件架构设计", "架构/接口/风险控制措施分配/SOUP 选型"),
    ("5.4 软件详细设计", "单元(SOUC)设计/编码标准/静态分析"),
    ("5.5 单元实现与验证", "单元测试/静态分析/代码审查"),
    ("5.6 软件集成与集成测试", "集成测试/测试环境/回归"),
    ("5.7 软件系统测试", "系统级测试/与风险管理关联/可用性(IEC 62366)"),
    ("5.8 软件发布", "发布说明/版本标识/回归分析/可追溯矩阵"),
    ("6. 软件维护", "变更控制/问题报告/安全更新/PMS 反馈回路"),
    ("7. 软件风险管理", "与 ISO 14971 衔接：风险控制措施的软件实现与验证"),
    ("8. 配置管理", "版本标识/构建可复现/变更追溯"),
    ("9. 问题解决", "问题报告/影响分析/纠正措施"),
]

SOUP_CHECKPOINTS = [
    "SOUP 清单：名称/版本/制造商/许可证",
    "已知异常（anomaly list）对预期用途的影响评估",
    "SOUP 变更对安全等级的影响复评",
    "网络安全暴露面（CVE 跟踪）与更新策略",
    "无 SOUP 场景下「自研轮子」的风险论证",
]


def classify(severity: int, probability: int) -> dict:
    """severity 1-5（5=死亡/严重伤害）；probability 1-5（仅记录，不参与分级）。

    IEC 62304:2006 §4.3：Class C 以**严重度**为据（可能导致死亡或严重伤害），
    与发生概率无关；概率信息供 ISO 14971 风险文件交叉引用。
    2026-10-12 复审修订：原 S5 且 P≥3 才判 C 的逻辑与标准定义矛盾，已改为
    S5 直接判 C（历史勘误）。
    """
    if not (1 <= severity <= 5 and 1 <= probability <= 5):
        raise ValueError("severity/probability 须 1–5")
    if severity >= 5:
        return {"Class": "C", "判据": "可能死亡/严重伤害（S5，按严重度判定，不问概率）",
                "要求": "全生命周期文档 + 单元级验证 + 严格变更控制"}
    if severity >= 3:
        return {"Class": "B", "判据": "可能非严重伤害（S3–S4）",
                "要求": "需求/架构/集成/系统测试 + 回归分析"}
    return {"Class": "A", "判据": "不可能导致伤害（S≤2）",
            "要求": "文档化开发过程即可（仍需记录判定依据）"}


def render_processes() -> str:
    lines = ["# IEC 62304 软件生命周期过程清单", ""]
    for name, desc in SW_PROCESSES:
        lines.append(f"- [ ] **{name}** — {desc}")
    lines += ["", "## SOUP 检查点", ""]
    for c in SOUP_CHECKPOINTS:
        lines.append(f"- [ ] {c}")
    return "\n".join(lines)


def _demo() -> int:
    print("IEC 62304 软件生命周期工具 · 演示\n")
    for sev, prob in [(5, 3), (3, 2), (1, 4)]:
        c = classify(sev, prob)
        print(f"  S{sev}×P{prob} → Class {c['Class']}（{c['判据']}）")
    print(f"\n### 生命周期过程（{len(SW_PROCESSES)} 项）")
    for name, desc in SW_PROCESSES[:4]:
        print(f"  - {name}: {desc}")
    print("\n[demo] 最终等级须结合 ISO 14971 风险管理文件判定。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="IEC 62304 软件生命周期工具")
    ap.add_argument("--demo", action="store_true", help="跑内置演示")
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--classify", action="store_true", help="安全等级判定")
    ap.add_argument("--severity", type=int, choices=range(1, 6))
    ap.add_argument("--probability", type=int, choices=range(1, 6))
    ap.add_argument("--processes", action="store_true", help="打印生命周期过程清单")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()

    if args.demo:
        return _demo()
    if args.classify:
        if args.severity is None or args.probability is None:
            print("[err] --classify 须配 --severity 与 --probability")
            return 2
        c = classify(args.severity, args.probability)
        for k, v in c.items():
            print(f"{k}: {v}")
        return 0
    if args.processes:
        print(render_processes())
        return 0
    ap.print_help()
    return 2


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, ['Class'], [], None), (['--classify', '--severity', '5', '--probability', '3'], 0, ['Class: C'], [], None), (['--classify', '--severity', '3', '--probability', '2'], 0, ['Class: B'], [], None), (['--classify', '--severity', '1', '--probability', '4'], 0, ['Class: A'], [], None), (['--classify'], 2, [], [], None), (['--classify', '--severity', '9', '--probability', '1'], 2, [], [], None)]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
