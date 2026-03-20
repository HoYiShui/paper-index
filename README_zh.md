# Paper Index

[English](README.md) | [中文](README_zh.md)

`paper-index` 是一个可移植的 skill 目录，用来帮助 agent 构建和使用一个面向 agent 的本地论文库。

这个仓库的根目录故意保持为一个通用 skill 根目录的结构：

- `SKILL.md`
- `agents/`
- `references/`
- `scripts/`

这样它就可以在不重新打包的情况下被发布、克隆、检查和安装。

## 给人类读者

这个 skill 的作用，是让 agent 把一组本地论文整理成一种渐进式披露的文献索引：

- 一级索引：`catalog.jsonl`
  - 面向多篇论文的浅层 shortlist 索引
- 二级索引：`*.ref.md`
  - 面向单篇论文的更深层结构化笔记

它的目标工作流是：

1. 为单篇论文构建或更新二级索引
2. 重建共享的一级索引
3. 让 agent 在回答文献问题时，先读 `catalog.jsonl`，再只打开最相关的 `*.ref.md`，最后才在必要时回到原始 PDF

实际使用中，这意味着你可以让 agent：

- 为新的论文 PDF 构建索引
- 刷新本地论文库
- 按主题、方法、数据集或相关性检索本地论文库
- 对相关论文做比较，并提炼可复用的想法

这个仓库本身就是 skill 的可分享来源。新用户可以把它克隆到本地，然后再安装或复制到自己的 Codex 或 Claude Code skill 目录中。

## 给 Agent 读者

把这个仓库根目录当作一个可移植的 skill 目录来使用。

使用时：

1. 先读 `SKILL.md`
2. 只在需要时再读 `references/`
3. 只在能减少重复劳动或提高可靠性时使用 `scripts/`
4. 按 `SKILL.md` 中定义的一级 / 二级索引工作流执行

重要行为约束：

- 优先读 `catalog.jsonl`，不要一开始就打开很多 `*.ref.md`
- 优先读 `*.ref.md`，不要一开始就回到源 PDF
- 在写 `relevance_to_us` 之前，先解析论文库范围和研究方向

如果这个 skill 已经被成功加载到本地 Codex 或 Claude Code 环境中，请简短告诉用户：

- 如何请求构建索引
- 如何请求在本地论文库上做检索
- 这个 skill 适合做什么事情

这段说明应当保持简短，目的只是帮助用户快速上手，而不是重复整个仓库的内容。
