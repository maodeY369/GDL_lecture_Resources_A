# 翻译进度

更新日期：2026-08-07

## 总体状态

| 阶段 | 状态 | 结果 |
|---|---|---|
| 工程审计与英文基线 | 完成 | 主入口、依赖和构建系统已确认；英文 pdfLaTeX/BibTeX 基线成功，160 页 |
| 中文工作区与构建支持 | 完成 | `zh-cn/` 保持英文工程结构；`book` 类不变；XeLaTeX/Fandol 构建成功 |
| 主入口可达正文翻译 | 完成 | 前言、记号、第 1--7 章自然语言全部翻译 |
| 未接入章节翻译 | 翻译及结构 QA 完成 | `geometricstability.tex` 已翻译，但英文源缺宏、图片和文献条目，不能纳入正式 clean build |
| 中文读者数学导读附录 | 完成 | 作为明确标识的中文版编辑增补置于正文之后、参考文献之前；内容、结构、编译及逐页视觉 QA 通过 |
| 全工程 QA | 完成 | `translation/final-full-qa.json`：`ok=true`、0 errors、0 warnings |
| 最终 clean build | 完成 | 142 页；0 fatal、0 undefined reference、0 undefined citation、0 missing file |
| PDF 与书签检查 | 完成 | 原 130 页已完成全书检查；最终版物理第 104--115 页重新逐页渲染，附录 10 页及前后衔接无覆盖、越界或错位，中文书签正常 |

## 分章状态

| 顺序 | 文件/章节 | 数学区域 | labels / refs / citations | 英文残留与术语 | 构建与 diff |
|---:|---|---:|---:|---|---|
| 0 | `main.tex` 前言、记号及中文本地化 | 37 | 0 / 0 / 3 | 通过 | 正式 clean build 通过；diff 通过 |
| 1 | `introduction.tex` 引言与高维学习 | 90 | 4 / 5 / 26 | 通过 | 正式 clean build 通过；diff 通过 |
| 2 | `geometricpriors.tex` 几何先验 | 384 | 15 / 26 / 9 | 通过 | 正式 clean build 通过；diff 通过 |
| 3 | `geometricdomains.tex` 几何域：5G | 785 | 27 / 56 / 46 | 通过 | 正式 clean build 通过；diff 通过 |
| 4 | `geometricmodels.tex` 几何深度学习模型 | 538 | 25 / 52 / 99 | 通过 | 已确认样章；正式 clean build 通过；diff 通过 |
| 5 | `geometricapplications.tex` 问题与应用 | 5 | 0 / 0 / 90 | 通过 | 正式 clean build 通过；diff 通过 |
| 6 | `historic.tex` 历史视角 | 23 | 0 / 1 / 158 | 通过 | 正式 clean build 通过；diff 通过 |
| 7 | `geometricstability.tex` 几何稳定性（未接入） | 201 | 12 / 12 / 27 | 通过 | 结构 QA 与临时 smoke 排版通过；正式编译受英文源缺失项阻塞；diff 通过 |
| A | `appendix/math-primer.tex` 数学概念导读（中文版增补） | 62 | 22 / 33 / 4 | 通过 | target-only 结构 QA 与正式 clean build 通过；逐页视觉检查通过 |

英文原稿对应的主入口可达正文合计 1,862 个数学区域、71 个 labels、140 个 refs、431 个 citation occurrences，均与英文源逐项一致。计入未接入章节后，合计为 2,063 / 83 / 152 / 458。中文版增补附录另有 62 个数学区域、22 个 labels、33 个 refs 和 4 个 citation occurrences，按 target-only 规则独立校验，不混入英中逐字相等统计。

## 最终结果

- 中文构建命令：`latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex`（在 `zh-cn/` 中运行）。
- 最终 PDF：`zh-cn/build/main.pdf`，142 页。
- PDF：142 页，39,523,014 字节；SHA-256：`7e4289809e9f17903eabcd86e1d2ab657c029b9502d08e31cd76ab40b1dcc94e`。
- 2026-08-07 排版复检：原 130 页全书检查结果继续有效；最终 clean build 后以 120 dpi 重新渲染物理第 104--115 页，逐页检查附录全部 10 页、前置空白页和参考文献首页。另以 140 dpi 复核公式引用本地化修正页；未发现文本重合、裁切、表格越界、孤立标题或结构错位。
- overfull hbox：英文基线 16 处、最大 13.22614pt；中文最终 6 处、最大 8.45117pt；无 overfull vbox。
- 全部 8 个英中对应正文文件及 1 个 target-only 附录文件的残留/术语/结构 QA：0 errors、0 warnings。
- `git diff --no-index --check`：8 个正文文件均无空白错误。
- 尚需人工决定是否修复并接入孤立章节，详见 `review-needed.md`。
