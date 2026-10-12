#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
model_router.py — 任务级模型路由决策器
=====================================
依据 rules/03 Model Router 档位映射，分析任务 → 输出应选模型 + 子任务分派参数。

诚实标注（不可绕过的事实）：
  - 主会话模型由用户在选择器锁定，**本工具不会自动切换主会话模型**。
  - 真正落地路由的方式：用 Agent 工具的 `model` 参数派子任务（现有能力）。
  - 本工具产出「路由建议 + 子任务 model 参数」，不得宣称已自动换模型。
"""
import sys
import json

# rules/03 档位映射：L0 轻量 / L1 通用 / L2 强推理
MODELS = {
    "L0": {"name": "qwen3.8-flash / deepseek-flash", "use": "简单问答/单点事实/翻译/格式转换"},
    "L1": {"name": "均衡模型(默认)", "use": "普通分析/归纳/单步推理/写作/简单代码/图片理解/长文档"},
    "L2": {"name": "qwen3.8-max / kimi-k3", "use": "架构设计/多步逻辑/高风险决策/复杂代码/深度推理"},
}

TYPE_MAP = {
    "简单问答": "L0", "翻译": "L0", "单点事实": "L0", "定义": "L0",
    "普通分析": "L1", "归纳": "L1", "单步推理": "L1", "写作": "L1", "代码": "L1",
    "图片理解": "L1", "长文档": "L1",
    "深度推理": "L2", "架构设计": "L2", "高风险决策": "L2", "复杂代码": "L2", "多步逻辑": "L2",
}

RISK_KEYWORDS = ["删除", "批量", "系统", "支付", "发消息", "格式化", "重置", "覆盖",
                 "强制", "权限", "凭据", "私钥", "对外", "不可逆", "强推"]


def analyze(task: str) -> dict:
    # 难度分档
    if any(k in task for k in ["架构", "设计", "多步", "复杂", "高风险", "决策",
                                "不可逆", "推理链", "排障", "debug", "根因"]):
        level = "L2"
    elif any(k in task for k in ["分析", "归纳", "对比", "写", "生成", "实现",
                                  "代码", "总结", "理解", "识别", "审查"]):
        level = "L1"
    else:
        level = "L0"
    # 任务类型
    task_type = "通用"
    for k, v in TYPE_MAP.items():
        if k in task:
            task_type = k
            break
    # 风险命中
    risk_hits = [k for k in RISK_KEYWORDS if k in task]
    risk = "L2-confirm" if risk_hits else "normal"
    m = MODELS[level]
    reason = f"任务类型={task_type}; 难度分档={level}; 选 {m['name']}（{m['use']}）"
    if risk == "L2-confirm":
        reason += f"; 命中高风险关键词 {risk_hits} → 需 L2 确认（rules/01 §0.11）"
    return {
        "level": level,
        "model": m["name"],
        "task_type": task_type,
        "risk": risk,
        "risk_keywords": risk_hits,
        "reason": reason,
        "subagent_model_param": {"L0": "lite", "L1": "default", "L2": "reasoning"}.get(level),
        "auto_switch_main_session": False,
        "note": "主会话不自切；用 Agent 工具 model 参数派子任务实现路由",
    }


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "分析这份日志找出异常并定位根因"
    print(json.dumps(analyze(task), ensure_ascii=False, indent=2))
