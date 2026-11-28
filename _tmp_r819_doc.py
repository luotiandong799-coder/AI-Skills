import io
p = r'D:\腾讯AI\skills\00_总目录_所有AI入口.md'
t = io.open(p, encoding='utf-8').read()

# insert text record before r818 text record
anchor = '- **2026-11-28（r818 三连轮落地）**'
assert anchor in t
text = ('- **2026-11-28（r819 三连轮落地）**：'
 '`engineering/vi-fact-verification` 1.22.0→**1.23.0**（r819A 生存分析：删失不是缺失/事件，右删失下 KM 乘积限 Ŝ(t)=∏(1−dᵢ/nᵢ) 用「末次观察时间+是否发生事件」两列，三假设含删失者生存前景相同不可检验且压低 S；中位=首次 S≤0.5、平均受随访长度限制、约30%死亡只能估<0.3分位，log-rank 整条曲线默认等权而 Gehan-Breslow/Tarone-Ware/Fleming-Harrington 权重须事前声明；Cox h(t|x)=h₀(t)exp(xᵀβ)，HR 乘性倍数非概率，PH 假设须 log-log/Schoenfeld 检验，违例改分层/扩展 Cox） · '
 '`meta/ri-retrospective` 2.15.0→**2.16.0**（r819B 鱼骨图/石川图：ASQ 七大质量工具之一、「分类穷举+归并」定性工具非根因判定器，产出候选因清单；Ishikawa 6M=Materials/Machinery/Methods/Measurement/Manpower/Mother Nature +Money 第七 M，中文变体 5M1E/8M/4P/4S，分类是可改脚手架；原因型鱼头在右问为什么、对策型鱼头在左问如何改善、整理问题型非因果；三弱点主观+非定量+同因多类，候选因标「有数据/仅经验」仅经验者不得进改进项） · '
 '`meta/mi-memory` 2.13.0→**2.14.0**（r819C 闪光灯记忆：Brown & Kulik 1977 记的是 reception event 非事件本身，六类 canonical categories=地点/活动/来源/自己情绪/他人情绪/后果，须与事件本体分字段；鲜明+高置信+持久均不蕴含准确，Neisser & Harsch 挑战者号高度不一致、9/11 2/3 年一致性降但重大扭曲仅 9%/7%、撒切尔 86% vs Hirst 0.63 口径差异大；机制争议未定论，Conway/Finkenauer 一般机制高效率编码说 vs 特殊机制说，9/11 支持 wrong time slice 不支持 consolidation，agent 高情绪条目不自动加权且转述第 N 版编号）；三轮9独点全「增＝加厚现有」0新建；按13模块固定顺序取 VI/RI/MI（KI论文域排除，避开 r818 TI/DI/EI）；每轮≥2独立域一手（StatsDirect+statsmodels 官方 WebFetch200 · ASQ 官方+食品伙伴网 WebFetch200 · ScienceDirect 9/11+科普中国 WebFetch200），NCBI 号错配弃用、biostathandbook/statology/medcalc 404、Wikiwand/Wikibooks WebFetch 本地回退禁用如实登记；VI §十四似然比与 RI r800A 变更分析正文下沉 references 留摘要节腾行；三技能 desc 1016/998/1018 均≤1024；豆包自留地WB0落地；经验按VI/RI/MI写入D盘module-memory各3条共9条；共学两写4份见 `memory/co-learn/workbuddy/2026-11-28_学习轮r819*.md`。\n')
t = t.replace(anchor, text + anchor, 1)

# insert row before r818 row
row_anchor = '| r818 | 2026-11-28 |'
assert row_anchor in t
row = ('| r819 | 2026-11-28 | VI 生存分析 / RI 鱼骨图 / MI 闪光灯记忆 | '
       '3技能加厚bump+3份references+2处旧节下沉+9条模块记忆+共学两写（按13模块顺序取VI/RI/MI） |\n')
t = t.replace(row_anchor, row + row_anchor, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('total 2 places registered r819')

# archive audit log
src = r'D:\腾讯AI\skills\memory\co-learn\workbuddy\2026-11-28_学习轮r819_生存分析与鱼骨图与闪光灯记忆.md'
dst = r'D:\腾讯AI\每日学习日志\WorkBuddy_审计\2026-11-28\2026-11-28_学习轮r819_生存分析与鱼骨图与闪光灯记忆.md'
import shutil
shutil.copyfile(src, dst)
print('archived', dst)
