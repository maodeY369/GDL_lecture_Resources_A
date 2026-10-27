# 全文中文翻译 QA 报告

日期：2026-08-07  
正式范围：`main.tex` 的完整 `\input` 链（含中文版编辑增补 `appendix/math-primer.tex`）；另对未接入的 `geometricstability.tex` 完成翻译和结构 QA。

## 结论

主入口可达的完整中文文档及数学概念导读附录已 clean build 并通过全工程 QA。`translation/final-full-qa.json` 为 `ok: true`、0 errors、0 warnings；8 个英中对应正文文件和 1 个 target-only 附录文件的英文残留、术语与结构报告均为 0 errors、0 warnings。正式中文 PDF 共 142 页。

未接入的 `geometricstability.tex` 已完成自然语言翻译，201 个数学区域及全部 labels/refs/citations 保持一致，但英文源自身缺少旧宏、图片及参考文献条目，不能声明为正式可编译章节；该限制没有带入主入口工程。

## 构建

英文原版命令：

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

基线实际使用 `-outdir=translation/baseline-build` 保存产物和日志。结果：退出码 0，160 页。

中文命令（在 `zh-cn/` 下）：

```text
latexmk -C -outdir=build main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

最终结果：退出码 0，142 页；PDF 为 `zh-cn/build/main.pdf`，大小 39,523,014 字节，SHA-256 为 `7e4289809e9f17903eabcd86e1d2ab657c029b9502d08e31cd76ab40b1dcc94e`。

## 分章 QA

| 文件 | 数学区域 | labels | refs | citations | 结构/残留/术语 | 编译状态 |
|---|---:|---:|---:|---:|---|---|
| `main.tex` | 37 | 0 | 0 | 3 | 通过 | 正式构建通过 |
| `introduction.tex` | 90 | 4 | 5 | 26 | 通过 | 正式构建通过 |
| `geometricpriors.tex` | 384 | 15 | 26 | 9 | 通过 | 正式构建通过 |
| `geometricdomains.tex` | 785 | 27 | 56 | 46 | 通过 | 正式构建通过 |
| `geometricmodels.tex` | 538 | 25 | 52 | 99 | 通过 | 正式构建通过 |
| `geometricapplications.tex` | 5 | 0 | 0 | 90 | 通过 | 正式构建通过 |
| `historic.tex` | 23 | 0 | 1 | 158 | 通过 | 正式构建通过 |
| `geometricstability.tex` | 201 | 12 | 12 | 27 | 通过 | 源工程限制，见下文 |
| `appendix/math-primer.tex`（中文版增补） | 62 | 22 | 33 | 4 | target-only 规则通过 | 正式构建通过 |

所有英中对应正文数学区域的类型、顺序、内容、对齐、换行和公式内 labels 均逐字一致。主入口可达英文对应正文的数学区域合计 1,862 个；计入孤立章节后为 2,063 个，不匹配数为 0。中文版增补附录的 62 个数学区域另行记录 hash `949d850f89a2b4f8d3727e1ebf3a716566b2636278932986ef1d6537b3f26fbf`，并通过环境、括号、标签和引用解析检查，不作为英文翻译一致性样本。

labels、refs、eqrefs、自定义引用宏、citation keys、input/include、图片路径、bibliography 资源和 URL 的集合及出现次数均一致。正式构建中 unresolved reference、unresolved citation 和 missing resource 均为 0。

## 构建日志对比

| 类别 | 英文基线 | 中文最终 | 增量 |
|---|---:|---:|---:|
| fatal error | 0 | 0 | 0 |
| undefined reference | 0 | 0 | 0 |
| undefined citation | 0 | 0 | 0 |
| missing file | 0 | 0 | 0 |
| `fancyhdr` warning | 155 | 135 | -20 |
| overfull hbox | 16 | 6 | -10 |
| underfull hbox | 28 | 29 | +1 |
| overfull vbox | 0 | 0 | 0 |
| underfull vbox | 36 | 23 | -13 |
| 普通 LaTeX warning | 4 | 3 | -1 |
| LaTeX font warning | 2 | 0 | -2 |
| `fontspec` warning | 0 | 2 | +2 |
| missing character | 0 | 3 | +3 |

中文 overfull hbox 最大值为 8.45117pt，低于英文基线最大值 13.22614pt。原先 17.7367pt、27.57133pt 和 64.81175pt 的三处中文长公式溢出已通过公式外的换行点消除，公式内容未变。

2 条 `fontspec` 提示来自 Fandol 字体的 CJK Script 声明。3 条 `U+0002` 提示来自 `geometricdomains.tex:188` 附近受保护数学内容在 XeLaTeX 下的既有表现；抽检页面未见可见缺字。二者均已记录，不造成 fatal、引用或资源错误。

## 英文残留、术语与保留词

- 活动自然语言英文残留：0；数学、注释、`comment` 环境、代码、URL、路径、参考文献及保留词均按规则排除。
- 术语一致性告警：0。
- 术语表共 204 条；数学导读附录新增 15 条，包括“格、规则网格、网格曲面、坐标图、嵌入空间、内蕴量、外在量、切向量、图 Laplacian、规范变换、节点重编号、局部坐标标架”等。
- 保留词表共 303 项；CNN、LSTM、RNN、GNN、Transformer、Fourier、Euclidean、Lipschitz、Convolutional Kernels Networks、Neural Tangent Kernels 等保持原样。
- `.bib`、citation key、模型名、数据集名、库名、标识符、文件路径和二进制资源均未修改。

## PDF 与书签检查

2026-08-07 使用 Poppler 将附录加入前的全部 130 个物理页以 100 dpi 渲染，按每组 10 页制作总览并逐页检查；另以 140 dpi 原尺寸复查所有自动几何扫描候选。扫描了 31,566 个词框，页面边界之外的词框为 0。检查发现并修复：

1. 物理第 5 页（正文页 1）：Erlangen Programme 长边注末行与后续 `Marquis (2009)` 边注重合；将后者下移 `2\baselineskip`。
2. 物理第 87 页（正文页 83）：猫图说明与 VGG-16 说明边注相互覆盖；将后者下移 `5\baselineskip`。

修复后重叠候选由 351 降至 334，物理第 5、87 页已从候选页集合中消失；剩余候选经原图复查均为公式上下标、图内文字或同一行字形边界的正常叠置。修复后除标题页日期和上述两页外，其余 127 页与修复前的 100 dpi 渲染逐像素一致。最终 clean build 后两处修复页与增量验证图逐像素一致。结果：

新增附录后，对最终 142 页 PDF 的物理第 104--115 页以 120 dpi 重新渲染并逐页检查，覆盖前置空白页、附录全部 10 页及参考文献首页。检查中发现工程自定义 `\eqref` 自动带出英文 `equation`，与附录前置的中文“式”重复；改用工程既有 `\plaineqref` 后，以 140 dpi 复核受影响的物理第 107、108、112、114 页，重复显示已消除。最终未发现文字重合、裁切、表格越界、孤立标题、异常空白或前后结构错位。附录 10 个小节及其中文顶层书签均可读取，目录中的附录标题和页码正常。附录产生的 3 条 `underfull hbox` 位于末页导航表的窄列换行，视觉检查确认边框、行列和文字均完整，不属于覆盖或越界。

- 中文字体、公式、图像、边注、表格和链接显示正常；
- 目录标题为“目录”，条目和页码正常；
- 图注前缀为“图”，参考文献标题为“参考文献”；
- 未再发现正文裁切、边注/图文覆盖或严重中文排版溢出；
- PDF 书签树可读取原 7 个顶层章节、全部小节及新增数学导读附录，中文标题正确。

## 孤立章节的源工程限制

`geometricstability.tex` 从未被 `main.tex` 引用。临时接入时依次确认：

1. 当前导言区未定义 `\bbx`、`\bby`、`\LD`、`\om`、`\dL`、`\argmin`；
2. `figures/fourier_unstab.pdf` 不存在；
3. 25 个唯一 citation keys 中有 23 个不在 `references.bib`；
4. 仅在临时分组中提供兼容宏并以占位框跳过缺失图片后，TeX 可排版到 136 页，但文献仍无法解析。

临时兼容层未保留在正式中文工程中；诊断日志为 `translation/stability-smoke-build.log`。因此，该章的翻译与结构 QA 可以确认，但正式编译验收必须等作者补齐源工程依赖或明确弃用该章。

## diff 审查

- `git diff --no-index --check` 对 8 个正文文件均为 0 空白错误。
- 数学、结构、引用、资源路径的自动 diff 由 `validate_translation.py` 逐文件完成。
- 图片、数据、二进制资源和 `references.bib` 未改动。

## `AGENTS.md` 完成标准

对主入口可达的正式文档，11 项完成标准全部满足：正文完成、保护区域完整、数学/引用一致、中文构建成功、无 fatal 或未说明引用错误、术语/审查记录/最终 diff/QA 报告均已完成。

对中文版编辑增补附录，`zh-cn/appendix/AGENTS.md` 的内容边界、术语、target-only 结构 QA、clean build 和逐页视觉 QA 标准全部满足；附录开头已明确说明其不属于英文原稿或原作者新增论述。

对未接入的 `geometricstability.tex`，翻译、保护区域、术语、diff 和结构 QA 已满足，但“正式中文工程成功编译”不满足，原因是英文源缺宏、缺图片和缺文献条目。若将“仓库中所有孤立作者文件”也纳入完成口径，则项目仍需人工解决这一源工程阻塞项。
