# LaTeX 工程审计

审计日期：2026-08-06

## 仓库与基线

- 当前目录不是 Git 仓库（`git status --short --branch` 返回 `fatal: not a git repository`），因此不存在可确认的中文分支或 worktree。
- 英文源文件保持不变；中文工作区位于 `zh-cn/`，只复制源 `.tex`、`references.bib` 与原始图像资源，未复制 `.git/`、`main.bbl` 或临时构建产物。
- 唯一主入口是 `main.tex`：它是唯一同时包含 `\documentclass` 和 `\begin{document}` 的 `.tex` 文件。
- 英文基线输出位于 `translation/baseline-build/`。基线 PDF 为 160 页。

## 文档类、宏包与排版

- 文档类：`\documentclass[11pt]{book}`。
- 主导言区宏包：`xcolor`、`amsmath`、`amssymb`、`natbib`、`graphicx`、`amsthm`、`tgpagella`、`emptypage`、`multirow`、`booktabs`、`fontenc`、`tcolorbox`、`microtype`、`hyperref`、`marginnote`、`fancyhdr`、`appendix`。
- `math_commands.tex` 额外加载 `amsmath`、`amsfonts`、`bm`，并集中定义数学符号与引用辅助宏。
- 本地没有 `.cls`、`.sty`、`.bst`、`latexmkrc`、Makefile、README 或 CI 构建配置；`book.cls`、`plainnat.bst` 等均来自 TeX Live。
- 自定义定理环境在 `main.tex` 中声明为 `theorem`、`remark`、`example`、`remarks`、`consequence`、`consequences`，但全文没有任何对应 `\begin{...}` 实例，也没有 `definition`、`lemma`、`proposition`、`corollary` 或 `proof` 实例。
- `math_commands.tex` 含大量仅服务于数学记号的 `\def`/`\newcommand`。可含自然语言的宏主要是 `\figref`、`\Figref`、`\secref`、`\Secref`、`\eqref`、`\Eqref`、`\chapref`、`\algref` 等引用显示宏；首轮样章不修改这些宏定义。

## 依赖图

```text
main.tex
├── math_commands.tex
├── introduction.tex
│   ├── geometricpriors.tex
│   ├── geometricdomains.tex
│   ├── geometricmodels.tex
│   ├── geometricapplications.tex
│   └── historic.tex
├── references.bib（通过 \bibliography{references}）
└── figures/（正文通过 \includegraphics 引用）

geometricstability.tex（完整作者章节，但当前未被主入口引用）
```

图像资源共 72 个：`figures/` 中 71 个（26 PDF、42 PNG、2 JPEG、1 JPG，共 49,062,985 字节），以及根目录 `fmm.png`。所有路径和二进制内容均保持不变。

## 构建系统与参考文献

- 现有工程无包装脚本；从导言区的 `fontenc`/`tgpagella` 与既有 `main.bbl` 判断，原工程使用 pdfLaTeX + BibTeX。
- 可重复的英文构建命令：`latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`。为保持英文源目录清洁，本次等价地使用 `-outdir=translation/baseline-build`，并追加一次 `pdflatex` 使目录与交叉引用稳定。
- 参考文献：`natbib` + `plainnat` + BibTeX；数据库为 `references.bib`。`.bib` 和 citation keys 不翻译。
- 基线无 fatal error、无未定义 reference/citation、无缺失图片。已有警告：155 次 `fancyhdr` headheight、16 个 overfull hbox、28 个 underfull hbox、36 个 underfull vbox、4 个普通 LaTeX warning、2 个字体 warning。

## 文件分类

- 作者正文：`main.tex` 的前言/记号、`introduction.tex`、`geometricpriors.tex`、`geometricdomains.tex`、`geometricmodels.tex`、`geometricapplications.tex`、`historic.tex`、未接入的 `geometricstability.tex`。
- 作者宏文件：`math_commands.tex`；默认视为结构/数学保护文件，不做首轮翻译。
- 第三方模板：无本地模板文件；TeX Live 的类、宏包和 BST 不属于翻译范围。
- 不可翻译：`references.bib`、图像文件、路径、URL、labels、citation keys、数学区域、宏名和程序标识符。
- 生成文件：根目录既有 `main.bbl` 以及构建产生的 `.aux/.log/.out/.toc/.fls/.fdb_latexmk/.pdf`；除基线记录目录外不进入 `zh-cn/` 源副本。

## 样章选择

选择 `geometricmodels.tex`（“Geometric Deep Learning Models”）。它是被主入口实际引用的完整顶层章节，按去除注释后的活动结构统计，共有 538 个数学区域（502 个行内公式、21 个 `equation`、3 个 `equation*`、1 个 `eqnarray*`、6 个 `$$...$$`、3 个 `align`、2 个 `align*`）、8 个 figure、25 个 label、52 个交叉引用命令和 99 个 citation key，并密集出现 CNN、GNN、RNN、LSTM、GRU、MLP、ReLU、ResNet、Transformer 等缩写或专名。工程本身没有定理/证明实例，因此无法选择同时包含定理与证明的章节。
