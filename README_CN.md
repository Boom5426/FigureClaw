# FigureClaw

[English](README.md) | 简体中文

<!-- Hero image slot: add FigureClaw.png to the repository root -->
![FigureClaw](FigureClaw.png)

让科研出图不再难：FigureClaw 专为科研高质量可视化打造，自动推荐最适合的数据图表，并一键生成可复现的 Python 绘图代码，助你轻松画出顶刊级好图。

## 为什么用 FigureClaw

科研自动化已经普及，但“好图难画”依然是最大痛点之一。

- 顶刊和普刊的显著差异之一，就是图表的质量和表达力。
- 很多科研人员和开发者并不擅长高质量可视化，成果表达受限。
- FigureClaw 让“顶刊级”可视化变得简单、自动、可复现，让你的成果脱颖而出。

你将获得：
- 统一的安装入口，agent 读 `setup.md` 即可开始
- 默认只推荐有本地可运行模板的图
- `sunburst`、`chord` 等暂不支持的图只作为概念选项，不假装能直接生成代码
- 自带示例、模板、参考数据、打包脚本和图源审计产物

## 60 秒快速上手

FigureClaw 当前默认按 Codex-first 路径组织首次安装。

让你的 agent 先读统一安装入口：

`Read https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/setup.md and set up FigureClaw for me.`

然后在仓库根目录直接跑统一 smoke test：

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

你会拿到：

- 当前可执行的 `primary_chart`
- 分组比较示例默认会落到 `"contrast_dot"`
- 配色建议
- 依赖信息
- 可运行的 Python 绘图代码

<details>
<summary>手动安装 Codex Skill</summary>

```bash
git clone https://github.com/Boom5426/FigureClaw.git ~/.codex/FigureClaw
mkdir -p ~/.codex/skills
ln -sfn ~/.codex/FigureClaw/skills/figure-recommender ~/.codex/skills/figure-recommender
```

创建软链接后重启 Codex，再回到 `~/.codex/FigureClaw` 重跑上面的 smoke test。

</details>

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
安装路径，并附带统一的安装后 smoke test。

## Install With Codex

在 Codex 里粘贴：

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

手动路径：

`~/.codex/skills/figure-recommender`

成功标准：

- `~/.codex/skills/figure-recommender` 已存在
- smoke test 输出包含 `"primary_chart"`
- 分组比较示例落到 `"contrast_dot"`
- 输出里包含 `"python_code"`

## Install With Claude

在 Claude Code 里粘贴：

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.claude/INSTALL.md`

手动路径：

`~/.claude/skills/figure-recommender`

## Install With Dr. Claw

1. 运行 `python3 skills/figure-recommender/scripts/package_skill.py`
2. 在 Dr. Claw Skills UI 上传生成的 `dist/figure-recommender.zip`
3. 让 Dr. Claw 发现打包后的 `SKILL.md`、模板、参考和示例

## 验证安装

在仓库根目录执行统一 smoke test：

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

确认输出里包含：

- `"primary_chart"`
- `"contrast_dot"`
- `"python_code"`

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

## 手动安装

首次接触项目时，优先走上面的统一入口和折叠的 Codex 手动安装块。只有在本地
安装链路出问题时，才直接去看具体的平台安装文档。

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
