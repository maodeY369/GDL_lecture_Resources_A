# Geometric Deep Learning 学习资源与中文翻译

本仓库整理了论文 **Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges** 的英文材料、简体中文翻译、可编译 LaTeX 源文件及翻译质量检查资料，供几何深度学习相关课程、阅读和术语对照使用。

> 中文版是非官方学习译本，不代表原作者立场。中文版末尾的“数学概念导读”是面向中文读者编写的编辑性增补，不属于英文原稿。

## 论文信息

- 标题：*Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges*
- 作者：Michael M. Bronstein、Joan Bruna、Taco Cohen、Petar Veličković
- arXiv：[arXiv:2104.13478v2](https://arxiv.org/abs/2104.13478v2)
- DOI：[10.48550/arXiv.2104.13478](https://doi.org/10.48550/arXiv.2104.13478)

## PDF 下载

| 版本 | PDF | 说明 |
|---|---|---|
| 英文版 | [下载英文 PDF](./en/Geometric_Deep_Learning_original_en.pdf) | 由仓库中的英文 LaTeX 源码构建 |
| 简体中文版 | [下载中文 PDF](./zh-cn/Geometric_Deep_Learning_zh-cn.pdf) | 完整中文翻译，并包含数学概念导读附录 |

如果 GitHub 无法在线预览大文件，请在 PDF 页面使用 **Download raw file**，或克隆仓库后从本地打开。

## 仓库结构

```text
.
├── en/
│   ├── main.tex
│   ├── *.tex
│   ├── references.bib
│   ├── figures/
│   └── Geometric_Deep_Learning_original_en.pdf
├── zh-cn/
│   ├── main.tex
│   ├── *.tex
│   ├── appendix/math-primer.tex
│   ├── references.bib
│   ├── figures/
│   └── Geometric_Deep_Learning_zh-cn.pdf
├── translation/
│   ├── glossary.csv
│   ├── style-guide.md
│   ├── progress.md
│   ├── qa-report.md
│   └── tools/validate_translation.py
├── LICENSE
└── README.md
```

## 本地编译

推荐安装带有 `latexmk`、pdfLaTeX、XeLaTeX 和 BibTeX 的完整 TeX Live。

英文版：

```powershell
cd en
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

中文版：

```powershell
cd zh-cn
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

中文版保持原 `book` document class，使用 XeLaTeX、`ctex` 和 TeX Live 自带的 Fandol 字体提供中文支持。

## 中文翻译原则

- 数学公式、数学符号、变量和算子保持原样；
- labels、refs、citation keys 和资源路径保持原样；
- CNN、GNN、LSTM、Fourier、Laplacian、Riemann、Euclidean 等缩写或专有词保持英文；
- 使用统一术语表和简体中文学术表达；
- 对英文正文与中文版执行数学区域、引用、环境、术语和编译日志检查；
- 中文附录按仅中文版增补内容单独校验，不混入英中逐字一致性统计。

翻译术语、风格约定和详细 QA 结果见 [`translation/`](./translation/) 目录。当前正式中文 PDF 已通过 clean build，未出现 fatal error、未解析引用或未解析文献。

## 已知限制

`geometricstability.tex` 是原始源包中未被 `main.tex` 引用的孤立章节。其英文源缺少若干宏定义、图片和参考文献条目，因此保留供研究和对照，但不属于两份正式 PDF 的构建链。

## 版权与许可说明

原论文正文、图像、参考文献及其相关材料的权利归原作者或相应权利人所有。arXiv 页面为该版本标注的是 [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/)。本仓库不声称以 MIT 许可重新授权原论文、原始图像或其中文译文。

仓库根目录的 [`LICENSE`](./LICENSE) 仅适用于仓库维护者有权许可的原创脚本、整理性说明和其他辅助材料，不取代原始作品的版权及许可条件。使用、转载或再分发前，请自行核对原始材料的许可条件及适用法律。

## 反馈

如发现翻译、术语、公式保护或排版问题，欢迎通过 GitHub Issues 提交具体文件位置和修改建议。
