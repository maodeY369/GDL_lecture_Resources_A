# 中文构建变更

## 正式保留的最小改动

1. 保留 `\documentclass[11pt]{book}`、原 Latin 字体、数学字体和版式宏包。
2. 在 `zh-cn/main.tex` 的 `fontenc` 后增加：

   ```latex
   \usepackage[UTF8,scheme=plain,fontset=fandol]{ctex}
   ```

   目的：使用 XeLaTeX 和 TeX Live 自带 Fandol 字体支持简体中文，避免机器专属字体。
3. 保留原 `book` 类并增加标准中文显示名称：`目录`、`图`、`表`、`参考文献`、`证明`，以及未实际使用的定理环境名称。该改动不改变环境名、counter 或编号机制。
4. `geometricpriors.tex` 的“几何深度学习蓝图”框因中文长度产生 overfull vbox；在框前局部分页、框内使用 `\small`，并小幅减小上下内边距。正文、公式、标签和引用未变。
5. 在 `geometricdomains.tex` 两处、`geometricmodels.tex` 一处长行内公式前增加公式外 `\linebreak[4]`。三处 overfull hbox 分别由 17.7367pt、27.57133pt、64.81175pt 消除；数学区域 hash 未改变。
6. 2026-08-07 全页视觉复查发现两组 `\marginnote` 相互覆盖：物理第 5 页的 Erlangen Programme 长边注与 `Marquis (2009)` 边注，以及物理第 87 页的猫图说明与 VGG-16 说明。分别给后一个边注增加 `[2\baselineskip]` 和 `[5\baselineskip]` 的局部垂直偏移。正文、图片尺寸、引用键、公式和页面数量均未改变。
7. 在正文 `\input{introduction}` 之后、参考文献之前调用 `\appendix` 并接入 `\input{appendix/math-primer}`。该文件是明确标识的中文版编辑增补，不对应英文原稿；未增加宏包、字体、图片或二进制资源，原 `book` 类和参考文献配置不变。
8. `validate_translation.py` 增加 `--target-only-files` 参数：中文版独有增补文件单独执行数学统计、标签/引用统计、环境/括号平衡、英文残留和术语检查，同时继续严格比较全部英中对应正文。环境名及其版式选项被排除出英文残留扫描，以免把 `tcolorbox` 键误报为正文。
9. 工程的 `\eqref` 宏会自动带出英文 `equation`；附录中在中文“式”之后改用工程既有的 `\plaineqref`，消除 PDF 中“式 equation A.3”一类中英重复。仅改变交叉引用的显示文本，label key、目标公式和链接均未改变。

## 构建命令

英文基线：

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=translation/baseline-build main.tex
```

中文正式构建（在 `zh-cn/` 中）：

```text
latexmk -C -outdir=build main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

## 最终验证

- 英文基线：退出码 0，160 页。
- 中文 clean build：退出码 0，142 页。
- 0 fatal、0 undefined reference、0 undefined citation、0 missing file。
- overfull hbox：英文 16 处、最大 13.22614pt；中文 6 处、最大 8.45117pt；双方 overfull vbox 均为 0。
- 新增 2 条 Fandol `fontspec` CJK Script 提示与 3 条受保护数学区域 U+0002 提示；均不造成可见中文缺字或构建失败。
- 原 130 页均已渲染完成全书视觉检查；最终 clean build 后另以 120 dpi 逐页检查物理第 104--115 页。附录 10 页及其与正文、参考文献的衔接无文字覆盖、裁切、表格越界或结构错位；附录中文书签、目录条目和参考文献首页正常。

## 未保留的临时诊断改动

为审计未接入的 `geometricstability.tex`，曾在临时分组中提供 6 个兼容宏，并用占位框绕过缺失的 `figures/fourier_unstab.pdf`。该设置仅证明除缺失依赖外的 TeX 排版可继续，未写入正式主入口；文献条目仍缺失。诊断日志保存为 `translation/stability-smoke-build.log`。

## 执行环境说明

通用包装脚本在 Windows 中文绝对路径的沙箱映射下无法写入部分 `.aux/.fls` 文件；在 `zh-cn/` 工作目录直接运行相同 `latexmk` 命令可稳定复现。这是执行环境路径问题，不是工程错误。
