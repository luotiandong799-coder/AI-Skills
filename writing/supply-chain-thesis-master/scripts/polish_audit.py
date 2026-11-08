"""学术表达与文本质量诊断（自研，方法吸收自公开项目，未复制其代码）

用法：
  python polish_audit.py 文档.docx                 # 诊断整篇
  python polish_audit.py 文档.docx --para 3        # 诊断第 3 个正段落
  python polish_audit.py 原.docx --compare 改.docx # 保量对比（字数比 + 数据/引用保护）

检查项：
  A 套话与泛化结尾（模式1）  B 段末总结套句（模式2）  C AI 高频词密度
  D 整齐三元并列  E 模糊归因（无出处）  F 句长突发度（标准差/均值）
  G 引用一致性（正文[n] ↔ 文献条目、断链、未被引用）
  H 正文加粗数量  I 段落长度分布

输出：markdown 诊断报告（stdout）
"""
import argparse
import re
import statistics
import sys

import docx

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# 模式1 泛化结尾 / 意义声明
GENERIC = ['具有重要意义', '意义深远', '影响深刻', '意义重大', '前景广阔', '未来可期',
           '具有广阔的发展空间', '提供了新思路', '开辟了新方向', '具有重要的理论意义',
           '具有重要的现实意义', '为相关领域的研究提供', '注入了新的活力', '奠定了坚实基础']
# 模式2 段末总结套句
SUMMARY_TAIL = ['综上所述', '由此可见', '不难发现', '可以看出', '因此可以得出结论', '总而言之', '综上']
# AI 高频词（模式12 常见词表，摘录）
AI_WORDS = ['赋能', '抓手', '闭环', '生态化', '深度融合', '全面提升', '有效提升',
            '显著提升', '进一步优化', '持续优化', '不断完善', '切实', '充分体现',
            '高度契合', '系统性地', '全方位', '多维度', '多元化', '护航', '夯实',
            '保驾护航', '提质增效', '降本增效', '有效保障', '有力支撑']
# 模糊归因
VAGUE_SRC = ['专家认为', '研究表明', '有关研究显示', '业内普遍认为', '数据显示', '实践证明']
CITE = re.compile(r'\[(\d+)(?:[-,，](\d+))?\]')


def ptext(p):
    """取段落全文（含 fldSimple/hyperlink 内的域文本，python-docx 的 p.text 会漏）"""
    return ''.join(t.text or '' for t in p._element.iter(W + 't')).strip()


def body_paragraphs(doc):
    out = []
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    txt = ptext(p)
                    if len(txt) >= 20 and not re.match(r'^\[\d+\]\s', txt):
                        out.append(p)
    return out


def sentence_lengths(text):
    sents = [s for s in re.split(r'[。！？；]', text) if len(s.strip()) >= 4]
    return [len(s) for s in sents]


def diagnose(doc, only=None):
    paras = body_paragraphs(doc)
    if only is not None:
        paras = [paras[only - 1]] if 0 < only <= len(paras) else []
    report = []
    total_hits = {'generic': [], 'tail': [], 'aiwords': [], 'triple': [], 'vague': []}
    lens = []
    bold = 0
    for idx, p in enumerate(paras, 1):
        txt = ptext(p)
        for k in GENERIC:
            if k in txt:
                total_hits['generic'].append((idx, k))
        for k in SUMMARY_TAIL:
            if txt.endswith(k) or (k in txt[-12:]):
                total_hits['tail'].append((idx, k))
        hit_words = [w for w in AI_WORDS if w in txt]
        if hit_words:
            total_hits['aiwords'].append((idx, hit_words))
        enum_hits = len(re.findall(r'[\u4e00-\u9fa5]{2,6}、[\u4e00-\u9fa5]{2,6}、[\u4e00-\u9fa5]{2,6}(?:、[\u4e00-\u9fa5]{2,6})*', txt))
        if enum_hits >= 2:
            total_hits['triple'].append(idx)
        for v in VAGUE_SRC:
            if v in txt and not CITE.search(txt):
                total_hits['vague'].append((idx, v))
        lens += sentence_lengths(txt)
        bold += sum(1 for r in p.runs if r.font.bold and r.text.strip())

    # 引用一致性
    full = "\n".join(ptext(p) for t in doc.tables for r in t.rows for c in r.cells for p in c.paragraphs)
    refs = [x for x in full.split('\n') if re.match(r'^\[\d+\]\s', x.strip())]
    ref_nums = {int(re.match(r'^\[(\d+)\]', x.strip()).group(1)) for x in refs}
    cited = set()
    for m in CITE.finditer("\n".join(ptext(p) for p in body_paragraphs(doc))):
        a = int(m.group(1))
        b = int(m.group(2)) if m.group(2) else a
        cited.update(range(a, b + 1))
    broken = sorted(n for n in cited if n not in ref_nums)
    uncited = sorted(n for n in ref_nums if n not in cited)

    cv = (statistics.pstdev(lens) / statistics.mean(lens)) if len(lens) > 1 else 0
    report.append(f"# 文本诊断报告\n")
    report.append(f"- 检查段落数：{len(paras)}　总字数（汉字）：{sum(len(ptext(p)) for p in paras)}")
    report.append(f"- 句长突发度：均值 {statistics.mean(lens):.1f} 字 / 标准差 {statistics.pstdev(lens):.1f} / 变异系数 {cv:.2f}"
                  f"（<0.35 偏均匀，属 AI 特征；0.4–0.8 更像人写）")
    report.append(f"- 正文加粗片段：{bold} 处（建议 ≤5 处/全文）\n")
    report.append("## 命中明细\n")
    report.append(f"| 类型 | 命中 | 位置与内容 |")
    report.append(f"|---|---|---|")
    report.append(f"| 泛化结尾/意义声明 | {len(total_hits['generic'])} | {total_hits['generic'][:6]} |")
    report.append(f"| 段末总结套句 | {len(total_hits['tail'])} | {total_hits['tail'][:6]} |")
    report.append(f"| AI 高频词 | {len(total_hits['aiwords'])} 段 | {[(i, w) for i, w in total_hits['aiwords'][:6]]} |")
    report.append(f"| 顿号列举过密（中性提示，≥2/段） | {len(total_hits['triple'])} | 段 {total_hits['triple'][:8]} |")
    report.append(f"| 模糊归因（无出处） | {len(total_hits['vague'])} | {total_hits['vague'][:6]} |")
    report.append(f"| 引用断链 | {len(broken)} | {broken} |")
    report.append(f"| 文献未被引用 | {len(uncited)} | {uncited} |")
    return "\n".join(report)


def count_refs(doc):
    return sum(1 for t in doc.tables for r in t.rows for c in r.cells for p in c.paragraphs
               if re.match(r'^\[\d+\]\s', ptext(p)))


def compare(orig_path, new_path):
    a = docx.Document(orig_path)
    b = docx.Document(new_path)
    ta = "\n".join(ptext(p) for p in body_paragraphs(a))
    tb = "\n".join(ptext(p) for p in body_paragraphs(b))
    ca, cb = len(re.findall(r'[\u4e00-\u9fa5]', ta)), len(re.findall(r'[\u4e00-\u9fa5]', tb))
    ratio = cb / ca if ca else 0
    cites_a = sorted(set(CITE.findall(ta)))
    cites_b = sorted(set(CITE.findall(tb)))
    nums_a = re.findall(r'\d+(?:\.\d+)?%?', ta)
    nums_b = re.findall(r'\d+(?:\.\d+)?%?', tb)
    lines = [
        "# 保量对比",
        f"- 原文字数（汉字）：{ca}　改后：{cb}　保留率：{ratio:.1%}　"
        f"{'✅ ≥92% 达标' if ratio >= 0.92 else '❌ 低于 92%，需补回论证或例证'}",
        f"- 引用标记：原文 {len(cites_a)} 组 → 改后 {len(cites_b)} 组 "
        f"{'✅ 未丢引用' if len(cites_b) >= len(cites_a) else '❌ 引用丢失'}",
        f"- 数字/数据：原文 {len(nums_a)} 个 → 改后 {len(nums_b)} 个 "
        f"{'✅ 数据保留' if len(nums_b) >= len(nums_a) else '⚠️ 数字减少，需人工确认是否误删'}",
        f"- 参考文献条目数：原文 {count_refs(a)} → 改后 {count_refs(b)} "
        f"{'✅ 条目数一致' if count_refs(a) == count_refs(b) else '❌ 条目数变化，需核对是否误删文献'}",
    ]
    return "\n".join(lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('doc')
    ap.add_argument('--para', type=int, default=None)
    ap.add_argument('--compare', default=None)
    a = ap.parse_args()
    if a.compare:
        print(compare(a.doc, a.compare))
    else:
        print(diagnose(docx.Document(a.doc), a.para))
