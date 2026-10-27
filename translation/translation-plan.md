# 翻译计划与执行结果

## 已执行顺序

1. 固化英文 pdfLaTeX/BibTeX 基线。
2. 建立 `zh-cn/` 安全副本和 XeLaTeX/Fandol 中文支持。
3. 以已确认样章 `geometricmodels.tex`、术语表、保留词和风格指南为标准。
4. 按主入口顺序完成 `main.tex` → `introduction.tex` → `geometricpriors.tex` → `geometricdomains.tex` → `geometricmodels.tex` → `geometricapplications.tex` → `historic.tex`。
5. 对每章执行数学、引用、环境、残留、术语、编译和 diff 闭环；失败项在进入下一章前修复。
6. 翻译未接入的 `geometricstability.tex`，完成结构 QA，并审计其独立编译阻塞项。
7. 执行全工程 clean build、逐文件残留/术语 QA、日志对比、PDF 页面与书签检查。
8. 在正文结束、参考文献之前加入明确标识为中文版编辑增补的数学概念导读，按“直观问题—最小定义—深度学习实例—适用边界—正文入口”组织。
9. 为 `zh-cn/appendix/` 建立局部 `AGENTS.md`，并对附录执行 target-only 结构 QA、最终 clean build 和逐页 PDF 视觉检查。

## 当前状态

主入口可达文档及中文版数学概念导读附录已经完成并满足正式交付条件。唯一剩余决策是是否将 `geometricstability.tex` 作为正式章节接入；这需要先补齐英文源缺失的宏、图片和文献数据，不能在翻译阶段猜测修复。

## 停止条件

本轮在全部主入口章节通过 clean build 与 QA、孤立章节完成翻译和结构 QA、所有待人工项完成汇总后停止；不擅自接入或虚构修复孤立章节依赖。
