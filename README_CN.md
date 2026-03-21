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

## 5 分钟跑通 Codex 首次使用

如果你是第一次在 Codex 里用 FigureClaw，目标不是“装完”，而是 5 分钟内真的跑出第一个推荐结果，并知道下一步怎么继续。

### 第 1 步：先让 Codex 安装它

在 Codex 里直接粘贴：

`Read https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/setup.md and set up FigureClaw for me.`

如果你不想让 agent 代劳，也可以展开下面的手动安装步骤自己执行。

<details>
<summary>手动安装 Codex Skill</summary>

```bash
git clone https://github.com/Boom5426/FigureClaw.git ~/.codex/FigureClaw
mkdir -p ~/.codex/skills
ln -sfn ~/.codex/FigureClaw/skills/figure-recommender ~/.codex/skills/figure-recommender
```

创建软链接后重启 Codex。

</details>

### 第 2 步：确认 Codex 能看到这个 skill

在终端执行：

```bash
test -L ~/.codex/skills/figure-recommender
```

这条命令没有输出是正常的。只要退出码是 `0`，就说明 Codex 的 skill 目录里已经挂上了 FigureClaw。

### 第 3 步：跑第一个内置示例

进入仓库根目录后执行：

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-file skills/figure-recommender/examples/briefs/grouped-comparison.json \
  --output json
```

这是整个项目最重要的第一次运行。它不是随便吐一段 demo 文本，而是在走 FigureClaw 的真实主流程：

1. 读取一个最小可用的 `figure_brief`
2. 选择当前最合适的主图
3. 选择配色
4. 生成可运行的 Python 绘图代码

### 第 4 步：第一次只看懂这 3 个字段就够了

运行完上面的命令后，先别被整段 JSON 吓到，先只看：

- `primary_chart`：系统最终推荐你实际去画的图
- `palette`：给这张图配的颜色方案
- `python_code`：已经生成好的 Python 绘图代码

对于内置的分组比较示例，你应该看到：

- `"primary_chart"`
- `"contrast_dot"`
- `"python_code"`

这表示 FigureClaw 已经从“图表推荐”走到了“代码生成”，不是只给一个口头建议。

### 第 5 步：马上把示例换成你自己的需求

先用最小 brief 试一次。你可以把下面这段直接保存成一个 json 文件再运行：

```json
{
  "story_goal": "compare_group_difference",
  "field_mapping": {
    "category": "condition",
    "value": "score"
  }
}
```

然后执行：

```bash
python3 skills/figure-recommender/scripts/generate_figure_response.py \
  --brief-json '{"story_goal":"compare_group_difference","field_mapping":{"category":"condition","value":"score"}}' \
  --output json
```

到这一步，你已经不是在“测试安装”，而是在真正使用 FigureClaw 了。

### 第 6 步：回到 Codex 里直接提需求

重启 Codex 后，可以直接这样说：

`Use the figure-recommender skill. I want to compare scores across treatment groups and generate runnable Python plotting code.`

如果你还没有自己的结构化输入，也没关系。FigureClaw 的默认用法就是先根据自然语言推一个最小 brief，再继续推荐和生成代码。

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

如果你只想最快跑通，优先看上面的“5 分钟跑通 Codex 首次使用”。

在 Codex 里粘贴：

`Fetch and follow instructions from https://raw.githubusercontent.com/Boom5426/FigureClaw/refs/heads/main/.codex/INSTALL.md`

手动路径：

`~/.codex/skills/figure-recommender`

成功标准：

- `~/.codex/skills/figure-recommender` 已存在
- smoke test 输出包含 `"primary_chart"`
- 分组比较示例落到 `"contrast_dot"`
- 输出里包含 `"python_code"`
- 你知道 `primary_chart` 是推荐图、`python_code` 是生成代码

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
