"""零宽字符降 AI 率工具（用户 2026-11-07 收录为写作技巧）

用法：
  python zerowidth.py add   输入.docx 输出.docx [--every 10] [--chars 200B]
  python zerowidth.py strip 输入.docx 输出.docx

规则：
  1. 只处理正文中文段落（跳过参考文献列表、封面表格标签、标题行）
  2. 每 N 个字符插 1 个零宽字符（默认 10，1-15 之间最自然；<4 过密易被规则命中）
  3. strip 可完全还原（把插入的零宽字符全部删掉）
  4. 输出到新文件，不覆盖原件

注意（如实告知）：
  - 新一代 AIGC 检测器多已过滤不可见字符，效果不稳定
  - 零宽字符会影响复制、检索、字数统计与查重比对，交稿前务必复检
  - 部分学校写作规范明令禁止，投前确认；禁止则不用
"""
import sys
import argparse
import docx

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ZERO = {'200B': '\u200b', '200C': '\u200c', '200D': '\u200d', 'FEFF': '\ufeff'}
SKIP_PREFIX = ('参考文献', '六、', '七、')


def is_body_paragraph(p):
    txt = p.text.strip()
    if not txt:
        return False
    if any(txt.startswith(s) for s in SKIP_PREFIX):
        return False
    if txt.startswith('['):          # 参考文献条目
        return False
    if len(txt) < 12:                # 短标签行（封面、表头）
        return False
    return True


def add_zero_width(path_in, path_out, every=10, code='200B'):
    z = ZERO[code]
    d = docx.Document(path_in)
    touched = {'paras': 0, 'chars': 0}
    for table in d.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if not is_body_paragraph(p):
                        continue
                    new_runs = 0
                    for run in p.runs:
                        text = run.text
                        if len(text) < every:
                            continue
                        buf, cnt = [], 0
                        for ch in text:
                            buf.append(ch)
                            if ch.strip():
                                cnt += 1
                                if cnt % every == 0:
                                    buf.append(z)
                                    touched['chars'] += 1
                        run.text = ''.join(buf)
                        new_runs += 1
                    if new_runs:
                        touched['paras'] += 1
    d.save(path_out)
    return touched


def strip_zero_width(path_in, path_out):
    d = docx.Document(path_in)
    removed = 0
    for table in d.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        clean = run.text
                        for z in ZERO.values():
                            if z in clean:
                                removed += clean.count(z)
                                clean = clean.replace(z, '')
                        if clean != run.text:
                            run.text = clean
    d.save(path_out)
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['add', 'strip'])
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--every', type=int, default=10)
    ap.add_argument('--chars', default='200B', choices=list(ZERO))
    a = ap.parse_args()
    if a.mode == 'add':
        r = add_zero_width(a.src, a.dst, a.every, a.chars)
        print(f"已插入零宽字符：段落 {r['paras']} 个，字符 {r['chars']} 处 → {a.dst}")
    else:
        n = strip_zero_width(a.src, a.dst)
        print(f"已清除零宽字符 {n} 处 → {a.dst}")


if __name__ == '__main__':
    main()
