# FigureClaw

[English](README.md) | 简体中文

<!-- Hero image slot: add FigureClaw.png to the repository root -->
![FigureClaw](FigureClaw.png)

一个面向科研出图场景的 executable-first 工具：优先返回当前就能生成可运行
Python 代码的图，而不是先推荐一个没有代码模板的复杂图。

## 为什么用 FigureClaw

- 安装入口统一，先让 agent 读 `setup.md` 就能开始
- 默认优先选择已经有本地模板的可执行图
- 对 `sunburst`、`chord` 这类暂不直出代码的图，只作为概念选择暴露
- 自带示例、模板、参考数据、打包脚本和图源审计产物

## 60 秒快速上手

让你的 agent 先读统一安装入口：

`Read https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/setup.md and set up FigureClaw for me.`

然后直接跑最小示例：

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

你会拿到：

- 当前可执行的 `primary_chart`
- 配色建议
- 依赖信息
- 可运行的 Python 绘图代码

## 能做什么图

当前已经内置可执行模板的图包括：

- 组间差异图
- 组成占比图
- 分布图
- 折线和多变量趋势图
- 热力图
- benchmark 散点图 + 误差棒
- 关系/网络类图

如果你显式要求 `sunburst` 或 `chord`，FigureClaw 会把它作为概念图保留，
同时仍然输出一个可执行主图的代码结果。

## 安装

推荐优先使用根目录的 [`setup.md`](setup.md)。它会按运行环境分流到正确的
安装路径，并附带安装后的验证步骤。

## Install With Codex

在 Codex 里粘贴：

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

手动路径：

`~/.codex/skills/figure-recommender`

## Install With Claude

在 Claude Code 里粘贴：

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md`

手动路径：

`~/.claude/skills/figure-recommender`

## Install With Dr. Claw

1. 运行 `python3 skills/figure-recommender/scripts/package_skill.py`
2. 在 Dr. Claw Skills UI 上传生成的 `dist/figure-recommender.zip`
3. 让 Dr. Claw 发现打包后的 `SKILL.md`、模板、参考和示例

## 使用流程

默认流程是：

1. 描述你想表达的图形目标
2. 解析或补全成结构化 `figure_brief`
3. 选择最合适的可执行主图
4. 选择兼容配色
5. 从本地模板生成 Python 绘图代码

最小 brief 形状：

```json
{
  "story_goal": "compare_group_difference",
  "field_mapping": {
    "category": "condition",
    "value": "score"
  }
}
```

默认值：

- `figure_role = paper-main`
- `style_mode = readable`
- `palette_mode = auto`

起步示例都放在
[`skills/figure-recommender/examples/briefs/`](skills/figure-recommender/examples/briefs/)。

## 它是怎么工作的

FigureClaw 当前遵循 executable-first 规则：

1. 归一化并校验一个 brief 对象
2. 对候选图做排序
3. 选择最合适的可执行 `primary_chart`
4. 如果用户显式要求复杂但暂不支持直出代码的图，则额外返回
   `conceptual_chart`
5. 用仓库内置模板生成 Python 代码

这样可以保证“主图”和“实际给出的代码”是对齐的。

## 仓库结构

- `setup.md`: 统一 agent 安装入口
- `skills/figure-recommender/`: 运行时包、模板、参考和示例
- `.codex/INSTALL.md`: Codex 安装入口
- `.claude/INSTALL.md`: Claude Code 安装入口
- `docs/source-audits/`: 图源 notebook 审计产物
- `tests/`: 回归、打包、校验和选图测试

## 开发

运行完整测试：

```bash
python3 -m pytest tests -q
```

重新打包 zip：

```bash
python3 skills/figure-recommender/scripts/package_skill.py
```

重新生成图源审计产物：

```bash
python3 skills/figure-recommender/scripts/export_source_notebooks.py \
  --output-dir docs/source-audits
```
